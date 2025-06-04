<template>
  <div class="chart-container">
    <div class="header-row"
      style="display: flex; justify-content: flex-end; align-items: center; margin-right: 10px; margin-top: 10px; margin-bottom: 10px;">
      <div class="radio-group" style="display: flex; gap: 10px;">
        <label><input type="radio" v-model="selectedTimeUnit" name="option" value="daily" /> {{
          trend.chartOptions.dailyUnit }}</label>
        <label><input type="radio" v-model="selectedTimeUnit" name="option" value="hourly" /> {{
          trend.chartOptions.hourUnit }}</label>
      </div>
    </div>

    <!-- Hourly View with Scroll -->
    <div v-if="selectedTimeUnit === 'hourly'">
      <div class="scrollbar-container" ref="scrollbarContainer">
        <div class="scrollbar" ref="scrollbar"></div>
      </div>
      <div class="chart-wrapper" ref="chartWrapper">
        <div class="scroll-container" ref="scrollContainer">
          <canvas ref="hourlyChartCanvas"></canvas>
        </div>
      </div>
      <div class="x-axis-labels-container" ref="xAxisLabels">
        <div class="assy-info">
          <div class="nameLabel">ASSY品番</div>
          <div class="valueLable">{{ props.partNumber }}</div>
        </div>
        <div class="x-axis-scroll" ref="xAxisScroll">
          <table class="labels-table">
            <tbody>
              <tr class="dates-row"></tr>
              <tr class="times-row"></tr>
              <tr class="values-row"></tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="!hasData" class="no-data-message">
        データがありません (No data available)
      </div>
    </div>
    <!-- Daily View -->
    <div v-else>
      <div class="scrollbar-container" ref="dailyScrollbarContainer">
        <div class="scrollbar" ref="dailyScrollbar"></div>
      </div>

      <div class="daily-chart-wrapper" ref="dailyChartWrapper">
        <div class="daily-scroll-container" ref="dailyScrollContainer">
          <canvas ref="dailyChartCanvas"></canvas>
        </div>
      </div>

      <div class="x-axis-labels-container" ref="dailyXAxisLabels">
        <div class="assy-info">
          <div class="nameLabel">ASSY品番</div>
          <div class="valueLable">{{ props.partNumber }}</div>
        </div>
        <div class="x-axis-scroll" ref="dailyXAxisScroll">
          <table class="labels-table">
            <tbody>
              <tr class="dates-row"></tr>
              <tr class="values-row"></tr>
            </tbody>
          </table>
        </div>
      </div>
      <div v-if="!hasData" class="no-data-message">
        データがありません (No data available)
      </div>
    </div>
  </div>
</template>

<script setup>

import { ref, watch, onBeforeUnmount, nextTick, computed } from 'vue';
import axios from 'axios';
import { Chart } from 'chart.js/auto';
import { format, parseISO, eachDayOfInterval, isAfter } from 'date-fns';
import annotationPlugin from 'chartjs-plugin-annotation';
import trendData from '@/assets/config/trend.yaml';

const trend = ref(trendData.trend);
Chart.register(annotationPlugin);

const selectedTimeUnit = ref('daily');

const props = defineProps({
  partNumber: String,
  process: String,
  startDate: [String, Date],
  endDate: [String, Date]
});

const hourlyChartCanvas = ref(null);
const dailyChartCanvas = ref(null);
const chartWrapper = ref(null);
const scrollContainer = ref(null);
let hourlyChartInstance = null;
let dailyChartInstance = null;
const apiData = ref([]);

const dailyScrollbarContainer = ref(null);
const dailyScrollbar = ref(null);
const dailyChartWrapper = ref(null);
const dailyScrollContainer = ref(null);
const dailyXAxisLabels = ref(null);
const dailyXAxisScroll = ref(null);

const hasData = computed(() => {
  return apiData.value && apiData.value.length > 0;
});

const processHourlyData = (rawData) => {
  if (!rawData || rawData.length === 0) {
    const now = new Date();
    return {
      labels: [[format(now, 'MM/dd'), format(now, 'H:mm')]],
      datasets: [{
        data: [null],
        backgroundColor: 'red',
        borderColor: 'red',
        borderWidth: 1,
        barThickness: 40
      }]
    };
  }

  const sortedData = [...rawData].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
  const labels = [];
  const values = [];

  sortedData.forEach(item => {
    if (item.timestamp && item.value !== null && item.value !== undefined) {
      const date = parseISO(item.timestamp);
      labels.push([format(date, 'MM/dd'), format(date, 'H:mm')]);
      values.push(item.value);
    }
  });

  return {
    labels,
    datasets: [{
      data: values,
      backgroundColor: 'red',
      borderColor: 'red',
      borderWidth: 1,
      barThickness: 40
    }]
  };
};

const processDailyData = (rawData) => {
  if (!rawData || rawData.length === 0) {
    const now = new Date();
    return {
      labels: [format(now, 'MM/dd')],
      datasets: [{
        data: [null],
        backgroundColor: 'red',
        borderColor: 'red',
        borderWidth: 1,
        barThickness: 40
      }]
    };
  }

  // Group data by day
  const dailyGroups = {};
  rawData.forEach(item => {
    if (item.timestamp && item.value !== null && item.value !== undefined) {
      const date = parseISO(item.timestamp);
      const dayKey = format(date, 'yyyy-MM-dd');

      if (!dailyGroups[dayKey]) {
        dailyGroups[dayKey] = {
          date: date,
          values: []
        };
      }
      dailyGroups[dayKey].values.push(item.value);
    }
  });

  // Determine date range
  let startDate = props.startDate ? new Date(props.startDate) : new Date(rawData[0].timestamp);
  let endDate = props.endDate ? new Date(props.endDate) : new Date(rawData[rawData.length - 1].timestamp);

  // Ensure start date is before end date
  if (isAfter(startDate, endDate)) {
    [startDate, endDate] = [endDate, startDate];
  }

  // Get all days in range
  const allDays = eachDayOfInterval({ start: startDate, end: endDate });

  const labels = [];
  const values = [];

  allDays.forEach(day => {
    const dayKey = format(day, 'yyyy-MM-dd');
    const label = format(day, 'MM/dd');

    if (dailyGroups[dayKey]) {
      const sum = dailyGroups[dayKey].values.reduce((acc, val) => acc + val, 0);
      const avgValue = sum / dailyGroups[dayKey].values.length;
      labels.push(label);
      values.push(avgValue);
    } else {
      labels.push(label);
      values.push(null);
    }
  });

  return {
    labels,
    datasets: [{
      data: values,
      backgroundColor: 'red',
      borderColor: 'red',
      borderWidth: 1,
      barThickness: 40
    }]
  };
};

const calculateCanvasWidth = (dataLength) => {
  const MIN_BAR_WIDTH = 60;
  const BAR_SPACING = 15;
  const MIN_CANVAS_WIDTH = 1200;
  return Math.max(MIN_CANVAS_WIDTH, dataLength * (MIN_BAR_WIDTH + BAR_SPACING) + 200);
};

const fetchThresholdData = async () => {
  try {
    if (!props.partNumber || !props.process) return null;
    const response = await axios.get('http://localhost:5000/api/nox_assy_inv_mgt_thresh', {
      params: { partNumber: props.partNumber, process: props.process }
    });
    return response.data?.[0] || null;
  } catch (error) {
    console.error('Error fetching threshold data:', error);
    return null;
  }
};

const getAnnotationOptions = (thresholdData) => {
  if (!thresholdData) return {};
  return {
    annotations: {
      upperLimit: {
        type: 'line',
        yMin: parseFloat(thresholdData['基準在庫上限数']),
        yMax: parseFloat(thresholdData['基準在庫上限数']),
        borderColor: '#febf03',
        borderWidth: 2,
        borderDash: [6, 6],
        label: { content: `Upper Limit: ${thresholdData['基準在庫上限数']}`, enabled: true, position: 'right' }
      },
      lowerLimit: {
        type: 'line',
        yMin: parseFloat(thresholdData['基準在庫下限数']),
        yMax: parseFloat(thresholdData['基準在庫下限数']),
        borderColor: '#f92020',
        borderWidth: 2,
        borderDash: [6, 6],
        label: { content: `Lower Limit: ${thresholdData['基準在庫下限数']}`, enabled: true, position: 'right' }
      },
      standard: {
        type: 'line',
        yMin: parseFloat(thresholdData['基準在庫数']),
        yMax: parseFloat(thresholdData['基準在庫数']),
        borderColor: '#00ae4b',
        borderWidth: 2,
        label: { content: `Standard: ${thresholdData['基準在庫数']}`, enabled: true, position: 'right' }
      }
    }
  };
};

const getCircleMarkerPlugin = () => ({
  id: 'topCircleMarker',
  afterDatasetsDraw(chart) {
    const { ctx, data, scales: { x, y } } = chart;
    ctx.save();
    data.datasets.forEach((dataset) => {
      dataset.data.forEach((value, index) => {
        if (value !== null) {
          const xPos = x.getPixelForValue(index);
          const yPos = y.getPixelForValue(value);
          const capWidth = 30;
          const capHeight = 2;
          ctx.fillStyle = 'black';
          ctx.fillRect(xPos - capWidth / 2, yPos - capHeight / 2, capWidth, capHeight);
          ctx.beginPath();
          ctx.arc(xPos, yPos, 8, 0, Math.PI * 2);
          ctx.fill();
        }
      });
    });
    ctx.restore();
  }
});

const getBackgroundColorPlugin = () => ({
  id: 'circleMarker',
  beforeDraw(chart) {
    const { ctx, chartArea, scales } = chart;
    const xAxis = scales.x;
    ctx.save();
    ctx.fillStyle = 'rgba(128,128,128,255)';
    ctx.fillRect(chartArea.left, xAxis.top, chartArea.right - chartArea.left, xAxis.bottom - xAxis.top);
    ctx.restore();
  },
  afterDraw(chart) {
    const { ctx, data, scales: { x, y } } = chart;
    ctx.save();
    data.datasets.forEach((dataset) => {
      dataset.data.forEach((value, index) => {
        if (value != null) {
          ctx.beginPath();
          ctx.arc(x.getPixelForValue(index), y.getPixelForValue(value) - 4, 4, 0, Math.PI * 2);
          ctx.fillStyle = 'black';
          ctx.fill();
        }
      });
    });
    ctx.restore();
  }
});

const createHourlyChart = async () => {
  await nextTick();
  if (hourlyChartInstance) hourlyChartInstance.destroy();

  if (!hourlyChartCanvas.value) return;

  const thresholdData = await fetchThresholdData();
  const hourlyData = processHourlyData(apiData.value);
  setupXAxisLabels(hourlyData.labels);

  const canvasWidth = calculateCanvasWidth(hourlyData.labels.length);
  hourlyChartCanvas.value.style.width = `${canvasWidth}px`;
  hourlyChartCanvas.value.style.height = '500px';
  hourlyChartCanvas.value.width = canvasWidth;
  hourlyChartCanvas.value.height = 500;

  const maxDataValue = Math.max(...hourlyData.datasets[0].data.filter(val => val !== null));
  const upperLimit = thresholdData ? parseFloat(thresholdData['基準在庫上限数']) : 0;
  const yAxisMax = Math.max(maxDataValue * 1.1, upperLimit * 1.1) || 10;

  hourlyChartInstance = new Chart(hourlyChartCanvas.value.getContext('2d'), {
    type: 'bar',
    data: hourlyData,
    plugins: [getCircleMarkerPlugin(), getBackgroundColorPlugin()],
    options: {
      responsive: false,
      maintainAspectRatio: false,
      layout: { padding: { left: 40, bottom: 40 } },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: context => Number(context.raw).toFixed(2) } },
        annotation: getAnnotationOptions(thresholdData)
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { display: true, color: '#ccc' },
          min: 0,
          max: yAxisMax,
          ticks: { precision: 0, stepSize: 1 }
        },
        x: {
          grid: { display: true, color: '#ccc' },
          ticks: { display: false, autoSkip: false }
        }
      }
    }
  });

  if (hourlyData.labels.length > 10 && scrollContainer.value) {
    scrollContainer.value.scrollLeft = canvasWidth;
  }
  await nextTick();
  setupScrollbar();
};

const createDailyChart = async () => {
  await nextTick();
  if (dailyChartInstance) dailyChartInstance.destroy();

  if (!dailyChartCanvas.value) return;

  const thresholdData = await fetchThresholdData();
  const dailyData = processDailyData(apiData.value);


  // setupDailyXAxisLabels(dailyData.labels);
  setupDailyXAxisLabels(dailyData.labels, dailyData.datasets[0].data);

  // Calculate required width - 75px per bar (60px bar + 15px spacing)
  const barWidth = 75;
  const canvasWidth = Math.max(1200, dailyData.labels.length * barWidth);

  // Set canvas dimensions
  dailyChartCanvas.value.width = canvasWidth;
  dailyChartCanvas.value.height = 500;
  // dailyChartCanvas.value.style.width = `${canvasWidth}px`;
  dailyChartCanvas.value.style.height = '500px';

  // Set scroll container width to match canvas
  if (dailyScrollContainer.value) {
    dailyScrollContainer.value.style.width = `${canvasWidth}px`;
    dailyScrollContainer.value.style.minWidth = '100%';
  }

  // Calculate chart height and limits
  const maxDataValue = Math.max(...dailyData.datasets[0].data.filter(val => val !== null));
  const upperLimit = thresholdData ? parseFloat(thresholdData['基準在庫上限数']) : 0;
  const yAxisMax = Math.max(maxDataValue * 1.1, upperLimit * 1.1) || 10;

  // Create chart
  dailyChartInstance = new Chart(dailyChartCanvas.value.getContext('2d'), {
    type: 'bar',
    data: dailyData,
    plugins: [getCircleMarkerPlugin(), getBackgroundColorPlugin()],
    options: {
      responsive: false,
      maintainAspectRatio: false,
      layout: { padding: { left: 40, bottom: 40 } },
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: context => Number(context.raw).toFixed(2) } },
        annotation: getAnnotationOptions(thresholdData)
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: { display: true, color: '#ccc' },
          min: 0,
          max: yAxisMax,
          ticks: { precision: 0, stepSize: 1 }
        },
        x: {
          grid: { display: true, color: '#ccc' },
          ticks: { display: false } // Hide default x-axis labels
        }
      }
    }
  });

  // Initialize scrolling
  await setupDailyScrollbar();

  // Scroll to the end if there's enough data
  if (dailyData.labels.length > 10 && dailyScrollContainer.value) {
    dailyScrollContainer.value.scrollLeft = canvasWidth;
  }
};

const setupDailyXAxisLabels = (labels, valuesData) => {
  const datesRow = dailyXAxisLabels.value?.querySelector('.dates-row');
  const valuesRow = dailyXAxisLabels.value?.querySelector('.values-row');
  if (!datesRow || !valuesRow) return;

  datesRow.innerHTML = '';
  valuesRow.innerHTML = '';

  const barWidth = 75; // Same as in createDailyChart

  labels.forEach((date, index) => {
    const dateCell = document.createElement('td');
    dateCell.className = 'date-label';
    dateCell.style.width = `${barWidth}px`;
    dateCell.textContent = date;
    datesRow.appendChild(dateCell);

    const valueCell = document.createElement('td');
    valueCell.className = 'value-label';
    valueCell.style.width = `${barWidth}px`;
    // Use the valuesData passed to the function
    valueCell.textContent = valuesData[index] !== null && valuesData[index] !== undefined
      ? valuesData[index].toFixed(0)
      : '-';
    valuesRow.appendChild(valueCell);
  });

  // Synchronize x-axis labels scrolling with chart scrolling
  const chartScrollElement = dailyChartWrapper.value;

  if (chartScrollElement && dailyXAxisScroll.value) {
    // Remove existing listener if any to prevent duplicates on re-render
    const existingListener = dailyXAxisScroll.value.__syncListener; // Store ref to listener
    if (existingListener) {
      chartScrollElement.removeEventListener('scroll', existingListener);
    }

    const newListener = () => {
      dailyXAxisScroll.value.scrollLeft = chartScrollElement.scrollLeft;
    };
    chartScrollElement.addEventListener('scroll', newListener);
    dailyXAxisScroll.value.__syncListener = newListener; // Store ref for cleanup
  }
};

// const setupDailyScrollbar = async () => {
//   await nextTick();

//   if (!dailyScrollContainer.value || !dailyScrollbar.value || !dailyScrollbarContainer.value) {
//     console.error('Scroll elements not found');
//     return;
//   }

//   const updateScrollbar = () => {
//     const container = dailyScrollContainer.value;
//     const scrollbarContainer = dailyScrollbarContainer.value;
//     const scrollbar = dailyScrollbar.value;

//     if (!container || !scrollbarContainer || !scrollbar) return;

//     const hasHorizontalScroll = container.scrollWidth > container.clientWidth;

//     if (hasHorizontalScroll) {
//       const scrollRatio = container.scrollLeft / (container.scrollWidth - container.clientWidth);
//       const scrollbarWidth = scrollbarContainer.clientWidth *
//         (container.clientWidth / container.scrollWidth);

//       scrollbar.style.width = `${Math.max(30, scrollbarWidth)}px`; // Minimum width of 30px
//       scrollbar.style.left = `${scrollRatio * (scrollbarContainer.clientWidth - scrollbarWidth)}px`;
//       scrollbarContainer.style.display = 'block';
//     } else {
//       scrollbarContainer.style.display = 'none';
//     }
//   };

//   // Initial update
//   updateScrollbar();

//   // Sync scrolling between chart and x-axis labels
//   const syncScroll = () => {
//     updateScrollbar();
//     if (dailyXAxisScroll.value) {
//       dailyXAxisScroll.value.scrollLeft = dailyScrollContainer.value.scrollLeft;
//     }
//   };

//   // Set up event listeners
//   dailyScrollContainer.value.addEventListener('scroll', syncScroll);
//   window.addEventListener('resize', updateScrollbar);

//   // Make scrollbar draggable
//   let isDragging = false;
//   let startX, startLeft;

//   dailyScrollbar.value.addEventListener('mousedown', (e) => {
//     isDragging = true;
//     startX = e.clientX;
//     startLeft = dailyScrollbar.value.offsetLeft;
//     document.body.style.cursor = 'grabbing';
//     e.preventDefault();
//   });

//   document.addEventListener('mousemove', (e) => {
//     if (!isDragging || !dailyScrollbar.value || !dailyScrollbarContainer.value) return;

//     const containerWidth = dailyScrollbarContainer.value.clientWidth;
//     const scrollbarWidth = dailyScrollbar.value.clientWidth;
//     const maxLeft = containerWidth - scrollbarWidth;
//     const newLeft = startLeft + (e.clientX - startX);
//     const clampedLeft = Math.max(0, Math.min(maxLeft, newLeft));

//     dailyScrollbar.value.style.left = `${clampedLeft}px`;

//     const scrollRatio = clampedLeft / maxLeft;
//     dailyScrollContainer.value.scrollLeft = scrollRatio *
//       (dailyScrollContainer.value.scrollWidth - dailyScrollContainer.value.clientWidth);
//   });

//   document.addEventListener('mouseup', () => {
//     isDragging = false;
//     document.body.style.cursor = '';
//   });

//   // Cleanup function
//   return () => {
//     dailyScrollContainer.value?.removeEventListener('scroll', syncScroll);
//     window.removeEventListener('resize', updateScrollbar);
//   };
// };

const setupDailyScrollbar = async () => {
  await nextTick(); // Ensure DOM is updated

  // Initial check: if any core element is null, return early
  if (!dailyChartWrapper.value || !dailyScrollbar.value || !dailyScrollbarContainer.value || !dailyXAxisScroll.value) {
    console.warn('Daily chart scroll elements not fully available yet. Retrying...');
    // You might want to add a small delay and re-attempt or rely on the watcher
    // For now, let's just return if not ready.
    return;
  }

  const chartScrollElement = dailyChartWrapper.value;

  const updateScrollbar = () => {
    // Crucial: Add checks directly inside updateScrollbar
    if (!chartScrollElement || !dailyScrollbarContainer.value || !dailyScrollbar.value) {
      console.warn('updateScrollbar: Missing scrollbar elements, cannot update.');
      return;
    }

    const container = chartScrollElement;
    const scrollbarContainer = dailyScrollbarContainer.value;
    const scrollbar = dailyScrollbar.value;

    const hasHorizontalScroll = container.scrollWidth > container.clientWidth;

    if (hasHorizontalScroll) {
      const scrollRatio = container.scrollLeft / (container.scrollWidth - container.clientWidth);
      const scrollbarWidth = scrollbarContainer.clientWidth *
                              (container.clientWidth / container.scrollWidth);

      scrollbar.style.width = `${Math.max(30, scrollbarWidth)}px`;
      scrollbar.style.left = `${scrollRatio * (scrollbarContainer.clientWidth - scrollbarWidth)}px`;
      scrollbarContainer.style.display = 'block';
    } else {
      scrollbarContainer.style.display = 'none';
    }
  };

  const syncDailyChartAndLabelsScroll = () => {
    // Crucial: Add checks directly inside syncDailyChartAndLabelsScroll
    if (!dailyXAxisScroll.value || !chartScrollElement) {
      console.warn('syncDailyChartAndLabelsScroll: Missing elements, cannot sync.');
      return;
    }
    dailyXAxisScroll.value.scrollLeft = chartScrollElement.scrollLeft;
    updateScrollbar();
  };

  // Initial updates after elements are confirmed to exist
  syncDailyChartAndLabelsScroll(); // Call once on setup to ensure initial state

  // Set up event listeners
  // Ensure we only add listeners once and clean them up
  // Use a flag or check if listener is already added to avoid duplicates if setupDailyScrollbar is called multiple times
  if (!chartScrollElement.__scrollListenerAdded) { // Custom flag to prevent duplicate listeners
    chartScrollElement.addEventListener('scroll', syncDailyChartAndLabelsScroll);
    chartScrollElement.__scrollListenerAdded = true; // Mark as added
  }

  if (!window.__resizeListenerAddedDaily) { // Custom flag for window resize
    window.addEventListener('resize', updateScrollbar);
    window.__resizeListenerAddedDaily = true;
  }

  // Make scrollbar draggable
  let isDragging = false;
  let startX, startLeft;

  // Add null checks for mouse events as well
  dailyScrollbar.value.addEventListener('mousedown', (e) => {
    if (!dailyScrollbar.value || !dailyScrollbarContainer.value) return; // Add check
    isDragging = true;
    startX = e.clientX;
    startLeft = dailyScrollbar.value.offsetLeft;
    document.body.style.cursor = 'grabbing';
    e.preventDefault();
  });

  document.addEventListener('mousemove', (e) => {
    if (!isDragging || !dailyScrollbar.value || !dailyScrollbarContainer.value || !chartScrollElement) return; // Add check
    const containerWidth = dailyScrollbarContainer.value.clientWidth;
    const scrollbarWidth = dailyScrollbar.value.clientWidth;
    const maxLeft = containerWidth - scrollbarWidth;
    const newLeft = startLeft + (e.clientX - startX);
    const clampedLeft = Math.max(0, Math.min(maxLeft, newLeft));

    dailyScrollbar.value.style.left = `${clampedLeft}px`;

    const scrollRatio = clampedLeft / maxLeft;
    chartScrollElement.scrollLeft = scrollRatio *
      (chartScrollElement.scrollWidth - chartScrollElement.clientWidth);
  });

  document.addEventListener('mouseup', () => {
    isDragging = false;
    document.body.style.cursor = '';
  });

  // Cleanup function for onBeforeUnmount
  onBeforeUnmount(() => { // Move cleanup here for better management
    if (chartScrollElement && chartScrollElement.__scrollListenerAdded) {
      chartScrollElement.removeEventListener('scroll', syncDailyChartAndLabelsScroll);
      chartScrollElement.__scrollListenerAdded = false;
    }
    if (window.__resizeListenerAddedDaily) {
      window.removeEventListener('resize', updateScrollbar);
      window.__resizeListenerAddedDaily = false;
    }
    // Also destroy chart instances here if they haven't been already
    if (hourlyChartInstance) hourlyChartInstance.destroy();
    if (dailyChartInstance) dailyChartInstance.destroy();
  });
};

const setupXAxisLabels = (labels) => {
  const datesRow = document.querySelector('.dates-row');
  const timesRow = document.querySelector('.times-row');
  const valuesRow = document.querySelector('.values-row');
  if (!datesRow || !timesRow || !valuesRow) return;

  datesRow.innerHTML = '';
  timesRow.innerHTML = '';
  valuesRow.innerHTML = '';

  const cellWidth = 75; // 60px bar + 15px spacing

  labels.forEach(([date, time], index) => {
    const dateCell = document.createElement('td');
    dateCell.className = 'date-label';
    dateCell.style.width = `${cellWidth}px`;
    dateCell.textContent = date;
    datesRow.appendChild(dateCell);

    const timeCell = document.createElement('td');
    timeCell.className = 'time-label';
    timeCell.style.width = `${cellWidth}px`;
    timeCell.textContent = time;
    timesRow.appendChild(timeCell);

    const valueCell = document.createElement('td');
    valueCell.className = 'value-label';
    valueCell.style.width = `${cellWidth}px`;
    valueCell.textContent = apiData.value[index]?.value?.toFixed(0) || '-';
    valuesRow.appendChild(valueCell);
  });

  const syncXAxisLabels = () => {
    const xAxisScroll = document.querySelector('.x-axis-scroll');
    if (xAxisScroll && scrollContainer.value) {
      xAxisScroll.scrollLeft = scrollContainer.value.scrollLeft;
    }
  };

  if (scrollContainer.value) {
    scrollContainer.value.addEventListener('scroll', syncXAxisLabels);
  }
};

const scrollbar = ref(null);
const scrollbarContainer = ref(null);


const setupScrollbar = () => {
  if (!scrollContainer.value || !scrollbar.value || !scrollbarContainer.value) return;

  const updateScrollbar = () => {
    if (scrollContainer.value.scrollWidth > scrollContainer.value.clientWidth) {
      const scrollRatio = scrollContainer.value.scrollLeft / (scrollContainer.value.scrollWidth - scrollContainer.value.clientWidth);
      const scrollbarWidth = scrollbarContainer.value.clientWidth * (scrollContainer.value.clientWidth / scrollContainer.value.scrollWidth);
      scrollbar.value.style.width = `${scrollbarWidth}px`;
      scrollbar.value.style.left = `${scrollRatio * (scrollbarContainer.value.clientWidth - scrollbarWidth)}px`;
      scrollbarContainer.value.style.display = 'block';
    } else {
      scrollbarContainer.value.style.display = 'none';
    }
  };

  scrollContainer.value.addEventListener('scroll', () => {
    updateScrollbar();
    document.querySelector('.x-axis-scroll').scrollLeft = scrollContainer.value.scrollLeft;
  });

  updateScrollbar();

  let isDragging = false;
  scrollbar.value.addEventListener('mousedown', (e) => {
    isDragging = true;
    document.body.style.cursor = 'grabbing';
    e.preventDefault();
  });

  document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    const containerRect = scrollbarContainer.value.getBoundingClientRect();
    const scrollbarWidth = scrollbar.value.clientWidth;
    let newLeft = e.clientX - containerRect.left - scrollbarWidth / 2;
    newLeft = Math.max(0, Math.min(containerRect.width - scrollbarWidth, newLeft));
    const scrollRatio = newLeft / (containerRect.width - scrollbarWidth);
    scrollContainer.value.scrollLeft = scrollRatio * (scrollContainer.value.scrollWidth - scrollContainer.value.clientWidth);
  });

  document.addEventListener('mouseup', () => {
    isDragging = false;
    document.body.style.cursor = '';
  });
  window.addEventListener('resize', updateScrollbar);
};


const fetchGraphData = async () => {
  try {
    if (!props.partNumber || !props.process || !props.startDate || !props.endDate) {
      apiData.value = [];
      await createCharts();
      return;
    }

    const formatDate = (date) => {
      const d = new Date(date);
      return `${d.getFullYear()}/${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getDate().toString().padStart(2, '0')}`;
    };

    const res = await axios.get('http://localhost:5000/api/wip-inventories-histories-new', {
      params: {
        partNumber: props.partNumber,
        process: props.process,
        startDate: formatDate(props.startDate),
        endDate: formatDate(props.endDate)
      },
      timeout: 10000
    });

    apiData.value = res.data?.data || [];
    await createCharts();
  } catch (error) {
    console.error('Error loading graph data:', error);
    apiData.value = [];
    await createCharts();
  }
};

const createCharts = async () => {
  if (selectedTimeUnit.value === 'hourly') {
    await createHourlyChart();
  } else {
    await createDailyChart();
  }
};

const exportToCSV = () => {
  if (!apiData.value.length) {
    alert('No data available to export');
    return;
  }

  const headers = ['Date', 'Time', 'Value'];
  const rows = apiData.value.map(item => [
    format(parseISO(item.timestamp), 'MM/dd'),
    format(parseISO(item.timestamp), 'H:mm'),
    item.value?.toFixed(0) || '-'
  ]);

  const csvContent = [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `inventory_data_${props.partNumber}_${format(new Date(), 'yyyyMMdd')}.csv`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

watch(() => [
  props.partNumber,
  props.process,
  props.startDate,
  props.endDate
], fetchGraphData, { immediate: true });

watch(selectedTimeUnit, createCharts);

onBeforeUnmount(() => {
  if (hourlyChartInstance) hourlyChartInstance.destroy();
  if (dailyChartInstance) dailyChartInstance.destroy();
});

defineExpose({ exportToCSV });


</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow-y: hidden;
  padding: 20px;
  background-color: #dcdcdc;
  border-radius: 8px;
  margin-top: 0;
  font-family: 'Noto Sans JP', sans-serif;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.chart-wrapper {
  width: 100%;
  height: calc(500px - 15px);
  overflow-x: hidden;
  border: 1px solid #eee;
  border-radius: 0 0 4px 4px;
  background: #dcdcdc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.daily-chart-wrapper {
  width: 100%;
  height: 500px;
  /* overflow: hidden; */
  overflow-x: auto;
  /* Changed from hidden to auto */
  overflow-y: hidden;
  /* Keep y-axis hidden */
  position: relative;
  background: #dcdcdc;
  border: 1px solid #eee;
  border-radius: 4px;
}

/* For WebKit browsers (Chrome, Safari, Edge) */
.daily-chart-wrapper::-webkit-scrollbar {
  display: none; /* Hide the scrollbar itself */
  width: 0;     /* Ensure no width is taken up by the scrollbar */
  height: 0;    /* Ensure no height is taken up by the scrollbar */
}

/* For Firefox */
.daily-chart-wrapper {
  scrollbar-width: none; /* Hide the scrollbar */
}

.daily-scroll-container {
  height: 100%;
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  scrollbar-width: none;
}

.x-axis-scroll {
  overflow-x: hidden;
  overflow-y: hidden;
  flex: 1;
  scrollbar-width: none;
}

.labels-table {
  border-collapse: collapse;
  width: max-content;
}

.labels-table tbody {
  display: block;
  border-bottom: #1c0808;
}

.labels-table tr {
  display: block;
  border-bottom: #1c0808;
}

.labels-table td {
  border: 1px solid #1c0808;
  text-align: center;
  padding: 4px 0;
  font-size: 13px;
  white-space: nowrap;
  height: 20px;
  min-width: 75px;
}

.scroll-container {
  height: 100%;
  min-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  position: relative;
  scrollbar-width: none;
}

.scrollbar-container {
  width: 100%;
  height: 15px;
  background: #f0f0f0;
  border-radius: 4px 4px 0 0;
  position: relative;
  margin-bottom: 2px;
}

.scrollbar {
  height: 11px;
  background: #888;
  border-radius: 4px;
  position: absolute;
  top: 2px;
  cursor: grab;
  transition: background 0.2s;
}

.scrollbar:hover {
  background: #555;
}

.scrollbar-container[style*="display: block"] {
  display: block !important;
}

.scroll-container::-webkit-scrollbar,
.x-axis-scroll::-webkit-scrollbar {
  display: none;
}

.value-label {
  text-align: center;
  font-weight: bold !important;
  font-size: 12px;
  color: black !important;
  background-color: red !important;
  padding: 4px 0;
  border: 1px solid #1c0808;
  height: 20px;
  display: inline-block;
}

.values-row {
  color: black !important;
  background-color: red !important;
  font-weight: bold !important;
}

.no-data-message {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 40px;
  text-align: center;
  color: #999;
  font-size: 1.1rem;
  z-index: 10;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 8px;
}

.x-axis-labels-container {
  display: flex;
  width: 100%;
  overflow: hidden;
  font-size: 14px;
  background: #808080;
  border-radius: 0 0 4px 4px;
}

.assy-info {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  min-width: 100px;
  background-color: #808080;
  padding: 10px;
  font-weight: bold;
  position: sticky;
  left: 0;
  z-index: 2;
  font-size: 12px;
}

.dates-row,
.times-row {
  display: flex;
  flex-direction: row;
  width: fit-content;
  background-color: #808080;
  border-bottom: #1c0808;
  font-weight: bold !important;
  font-size: 12px;
}

.dates-row{
  margin-bottom: 15px;
}

.times-row{
    margin-top: 5px;
}

.date-label,
.time-label {
  width: 75px;
  text-align: center;
  padding: 4px 0;
  font-size: 13px;
  white-space: nowrap;
  border-left: 1px solid #ccc;
}
</style>
