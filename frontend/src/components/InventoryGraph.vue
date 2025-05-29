<template>
  <div class="chart-container">
    <div class="header-row"
      style="display: flex; justify-content: flex-end; align-items: center; margin-right: 10px; margin-top: 10px; margin-bottom: 10px;">
      <div class="radio-group" style="display: flex; gap: 10px;">
        <label><input type="radio" name="option" value="a" /> {{ trend.chartOptions.dailyUnit }}</label>
        <label><input type="radio" name="option" value="b" /> {{ trend.chartOptions.hourUnit }}</label>
      </div>
    </div>
    <!-- Scrollbar container above the chart -->
    <div class="scrollbar-container" ref="scrollbarContainer">
      <div class="scrollbar" ref="scrollbar"></div>
    </div>
    <div class="chart-wrapper" ref="chartWrapper">
      <div class="scroll-container" ref="scrollContainer">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
    <div class="x-axis-labels-container" ref="xAxisLabels">
      <div class="assy-info">
        <div>ASSY品番</div>
        <div>{{ props.partNumber }}</div>
      </div>
      <div class="x-axis-scroll" ref="xAxisScroll">
        <div class="labels-wrapper">
          <div class="dates-row"></div>
          <div class="times-row"></div>
        </div>
      </div>
    </div>
    <div v-if="!hasData" class="no-data-message">
      データがありません (No data available)
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick, computed } from 'vue';
import axios from 'axios';
import { Chart } from 'chart.js/auto';
import { format, parseISO } from 'date-fns';
import annotationPlugin from 'chartjs-plugin-annotation';
import trendData from '@/assets/config/trend.yaml'

const trend = ref(trendData.trend)
Chart.register(annotationPlugin);


const props = defineProps({
  partNumber: String,
  process: String,
  startDate: [String, Date],
  endDate: [String, Date]
});

const chartCanvas = ref(null);
const chartWrapper = ref(null);
const scrollContainer = ref(null);
let chartInstance = null;
const apiData = ref([]);

const hasData = computed(() => {
  return apiData.value && apiData.value.length > 0;
});

const processApiData = (rawData) => {
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

  // Convert API data to chart format
  const sortedData = [...rawData].sort((a, b) => {
    return new Date(a.timestamp) - new Date(b.timestamp);
  });

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

const calculateCanvasWidth = (dataLength) => {
  const MIN_BAR_WIDTH = 60;
  const BAR_SPACING = 15;
  const MIN_CANVAS_WIDTH = 1200;

  return Math.max(
    MIN_CANVAS_WIDTH,
    dataLength * (MIN_BAR_WIDTH + BAR_SPACING) + 200
  );
};

const createChart = async () => {
  await nextTick();

  if (chartInstance) {
    chartInstance.destroy();
  }
  await nextTick();

  // Return if canvas element is not available
  if (!chartCanvas.value) return;

  // Process the data (will handle empty data case)
  const chartData = processApiData(apiData.value);

  setupXAxisLabels(chartData.labels);

  // Set up canvas dimensions
  const dataLength = Math.max(chartData.labels.length, 1);
  const canvasWidth = calculateCanvasWidth(dataLength);

  chartCanvas.value.style.width = `${canvasWidth}px`;
  chartCanvas.value.style.height = '500px';
  chartCanvas.value.width = canvasWidth;
  chartCanvas.value.height = 500;

  const ctx = chartCanvas.value.getContext('2d');
  chartCanvas.value.style.width = `${canvasWidth}px`;
  chartCanvas.value.style.height = '500px';
  chartCanvas.value.width = canvasWidth;
  chartCanvas.value.height = 500;

  if (dataLength > 10 && scrollContainer.value) {
    // scrollContainer.value.scrollLeft = canvasWidth;
    if (scrollContainer.value) {
      scrollContainer.value.scrollLeft = canvasWidth;
    }

  }

  // Setup scrollbar after chart is created
  await nextTick();
  setupScrollbar();

  // Custom plugin for top black circles
  const circleMarkerPlugin = {
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
            const capY = yPos - capHeight / 2;
            ctx.fillStyle = 'black';
            ctx.fillRect(xPos - capWidth / 2, capY, capWidth, capHeight);
            const radius = 8;
            ctx.beginPath();
            ctx.arc(xPos, yPos, radius, 0, Math.PI * 2);
            ctx.fillStyle = 'black';
            ctx.fill();

          }
        });
      });
      ctx.restore();
    }
  };

  const backgroundColorPlugin = {
    id: 'circleMarker',
    beforeDraw(chart) {
      const { ctx, chartArea, scales } = chart;
      const xAxis = scales.x;

      ctx.save();
      ctx.fillStyle = 'rgba(128,128,128,255)';
      const yTop = xAxis.top;
      const yBottom = xAxis.bottom;

      ctx.fillRect(chartArea.left, yTop, chartArea.right - chartArea.left, yBottom - yTop);
      ctx.restore();
    },
    afterDraw(chart) {
      const { ctx, data, scales: { x, y } } = chart;
      ctx.save();
      data.datasets.forEach((dataset) => {
        dataset.data.forEach((value, index) => {
          if (value != null) {
            const xPosition = x.getPixelForValue(index);
            const yPosition = y.getPixelForValue(value);
            ctx.beginPath();
            ctx.fillStyle = 'black';
            const radius = 4;
            ctx.arc(xPosition, yPosition - radius, radius, 0, Math.PI * 2);
            ctx.fill();
          }
        });
      });
      ctx.restore();
    }
  };


  chartInstance = new Chart(ctx, {
    type: 'bar',
    data: chartData,
    plugins: [circleMarkerPlugin, backgroundColorPlugin],
    options: {
      responsive: false,
      maintainAspectRatio: false,
      layout: {
        padding: {
          bottom: 40
        }
      },
      plugins: {
        legend: {
          display: false,
          position: 'top'
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              return `${context.raw}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          grid: {
            display: true,
            color: '#ccc'
          },
          title: {
            display: true,
          },
          min: 0,
          max: Math.max(...chartData.datasets[0].data.filter(val => val !== null)) * 1.1 || 10
        },
        x: {
          grid: {
            display: true,
            color: '#ccc'

          },
          title: {
            display: false,
          },
          ticks: {
            display: false,
            autoSkip: false,
            maxRotation: 0,
            minRotation: 0,
            color: 'black',
            font: {
              weight: 'bold'
            }
          }
        }
      }
    }
  });

  if (dataLength > 10 && scrollContainer.value) {
    scrollContainer.value.scrollLeft = canvasWidth;
  }
};

const fetchGraphData = async () => {
  try {
    // Validate required parameters
    if (!props.partNumber || !props.process || !props.startDate || !props.endDate) {
      apiData.value = [];
      return;
    }

    // Format dates for API request
    const formatDate = (date) => {
      if (!date) return '';
      const d = new Date(date);
      return `${d.getFullYear()}/${(d.getMonth() + 1).toString().padStart(2, '0')}/${d.getDate().toString().padStart(2, '0')}`;
    };

    const params = {
      partNumber: props.partNumber,
      process: props.process,
      startDate: formatDate(props.startDate),
      endDate: formatDate(props.endDate)
    };

    const res = await axios.get('http://localhost:5000/api/wip-inventories-histories-new', {
      params,
      timeout: 10000
    });

    if (res.data && res.data.data) {
      apiData.value = res.data.data;
      await createChart();
      // setupXAxisLabels(processApiData(res.data.data).labels);
    } else {
      apiData.value = [];
    }

    await createChart();

  } catch (error) {
    console.error('Error loading graph data:', error);
    apiData.value = [];
    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }
  }
};

watch(() => [
  props.partNumber,
  props.process,
  props.startDate,
  props.endDate
], fetchGraphData, { immediate: true });

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});

onMounted(() => {
  fetchGraphData();
});


const scrollbar = ref(null);
const scrollbarContainer = ref(null);

const setupScrollbar = () => {
  if (!scrollContainer.value || !scrollbar.value || !scrollbarContainer.value) return;

  const updateScrollbar = () => {
    if (!scrollContainer.value || !scrollbar.value || !scrollbarContainer.value) return;

    // Check if scrollWidth is greater than clientWidth (content is scrollable)
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
    const xAxisLabels = document.querySelector('.x-axis-labels-container');
    if (xAxisLabels) {
      xAxisLabels.scrollLeft = scrollContainer.value.scrollLeft;
    }
  });

  // Initialize scrollbar
  updateScrollbar();

  scrollContainer.value.addEventListener('scroll', updateScrollbar);

  let isDragging = false;

  scrollbar.value.addEventListener('mousedown', (e) => {
    isDragging = true;
    document.body.style.cursor = 'grabbing';
    e.preventDefault();
  });

  document.addEventListener('mousemove', (e) => {
    if (!isDragging || !scrollContainer.value || !scrollbar.value || !scrollbarContainer.value) return;

    const containerRect = scrollbarContainer.value.getBoundingClientRect();
    const relativeX = e.clientX - containerRect.left;
    const scrollbarWidth = scrollbar.value.clientWidth;
    let newLeft = relativeX - scrollbarWidth / 2;

    // Constrain to container
    newLeft = Math.max(0, Math.min(containerRect.width - scrollbarWidth, newLeft));

    const scrollRatio = newLeft / (containerRect.width - scrollbarWidth);
    scrollContainer.value.scrollLeft = scrollRatio * (scrollContainer.value.scrollWidth - scrollContainer.value.clientWidth);
  });

  document.addEventListener('mouseup', () => {
    isDragging = false;
    document.body.style.cursor = '';
  });

  // Update on resize
  window.addEventListener('resize', updateScrollbar);
};

// const setupXAxisLabels = (labels) => {
//   if (!labels || !labels.length || !scrollContainer.value || !chartCanvas.value) return;

//   const datesRow = document.querySelector('.dates-row');
//   const timesRow = document.querySelector('.times-row');

//   // Clear existing labels
//   datesRow.innerHTML = '';
//   timesRow.innerHTML = '';

//   // Calculate bar width and spacing
//   const barWidth = 60; // Should match your chart's bar width
//   const barSpacing = 15; // Should match your chart's bar spacing

//   labels.forEach(([date, time]) => {
//     // Create date label
//     const dateLabel = document.createElement('div');
//     dateLabel.className = 'date-label';
//     dateLabel.textContent = date;
//     dateLabel.style.width = `${barWidth + barSpacing}px`;
//     datesRow.appendChild(dateLabel);

//     // Create time label
//     const timeLabel = document.createElement('div');
//     timeLabel.className = 'time-label';
//     timeLabel.textContent = time;
//     timeLabel.style.width = `${barWidth + barSpacing}px`;
//     timesRow.appendChild(timeLabel);
//   });

//   // Sync scrolling
//   scrollContainer.value.addEventListener('scroll', () => {
//     const xAxisLabels = document.querySelector('.x-axis-labels-container');
//     if (xAxisLabels) {
//       xAxisLabels.scrollLeft = scrollContainer.value.scrollLeft;
//     }
//   });
// };
const setupXAxisLabels = (labels) => {
  const datesRow = document.querySelector('.dates-row');
  const timesRow = document.querySelector('.times-row');
  if (!datesRow || !timesRow) return;

  // Clear previous
  datesRow.innerHTML = '';
  timesRow.innerHTML = '';

  const labelWidth = 75;

  labels.forEach(([date, time]) => {
    const dateDiv = document.createElement('div');
    dateDiv.className = 'date-label';
    dateDiv.style.width = `${labelWidth}px`;
    dateDiv.textContent = date;

    const timeDiv = document.createElement('div');
    timeDiv.className = 'time-label';
    timeDiv.style.width = `${labelWidth}px`;
    timeDiv.textContent = time;

    datesRow.appendChild(dateDiv);
    timesRow.appendChild(timeDiv);
  });

  // const scrollSync = () => {
  //   const xAxisScroll = document.querySelector('.x-axis-scroll');
  //   if (xAxisScroll && scrollContainer.value) {
  //     xAxisScroll.scrollLeft = scrollContainer.value.scrollLeft;
  //   }
  // };

  // scrollContainer.value.addEventListener('scroll', scrollSync);
  const syncXAxisLabels = () => {
    const xAxisScroll = document.querySelector('.labels-wrapper');
    if (xAxisScroll && scrollContainer.value) {
      xAxisScroll.style.transform = `translateX(-${scrollContainer.value.scrollLeft}px)`;
    }
  };

  scrollContainer.value.addEventListener('scroll', syncXAxisLabels);

};


</script>

<style scoped>
/* Keep your existing styles */
.chart-container {
  position: relative;
  width: 100%;
  height: 100vh;

  /* Full screen height */
  overflow-y: hidden;

  /* Prevent vertical scrollbar */
  padding: 20px;
  background-color: #dcdcdc;
  border-radius: 8px;
  margin-top: 0;

  /* Optional: remove if it causes scrolling */
  font-family: 'Noto Sans JP', sans-serif;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.chart-wrapper {
  width: 100%;
  height: calc(500px - 15px);

  /* overflow-x: auto; */
  overflow-x: hidden;
  border: 1px solid #eee;
  border-radius: 0 0 4px 4px;
  background: #dcdcdc;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.x-axis-scroll {
  /* overflow-x: auto; */
  overflow: hidden;
  flex: 1;
}

.labels-wrapper {
  display: flex;
  flex-direction: column;
  min-width: 100%;
}

.scroll-container {
  height: 100%;
  min-width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  position: relative;
  scrollbar-width: none;
  /* Hide scrollbar for Firefox */
}

/* Scrollbar container styles */
.scrollbar-container {
  width: 100%;
  height: 15px;
  background: black;
  border-radius: 4px 4px 0 0;
  overflow-x: hidden;
  position: relative;
  display: none;
}

.scrollbar {
  height: 8px;
  background: #888;
  border-radius: 4px;
  position: absolute;
  top: 3px;
  cursor: grab;
}

.scrollbar:hover {
  background: #555;
}

.scroll-container::-webkit-scrollbar {
  display: none;
  /* Hide scrollbar for Chrome/Safari */
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

.chart-wrapper::-webkit-scrollbar {
  height: 8px;
}

.chart-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.chart-wrapper::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.chart-wrapper::-webkit-scrollbar-thumb:hover {
  background: #555;
}


.x-axis-labels-container {
  /* display: flex;
  background-color: #dcdcdc;
  padding: 5px 0;
  position: relative;
  overflow-x: hidden;
  scrollbar-width: none; */

  display: flex;
  width: 100%;
  overflow: hidden;
  background-color: #808080;
  border-top: 2px solid #808080;
  border-bottom: 2px solid #aaa;
  font-size: 14px;
}

.x-axis-labels-container::-webkit-scrollbar {
  display: none;
  /* Hide scrollbar for Chrome/Safari */
}

.assy-info {
  /* display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 0 10px;
  min-width: 120px;
  background-color: #dcdcdc;
  position: sticky;
  left: 0;
  z-index: 2; */

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
  /* display: flex;
  background-color: #dcdcdc; */

  display: flex;
  flex-direction: row;
  width: fit-content;
  background-color: #808080;
}

.date-label,
.time-label {
  /* min-width: 60px;
  text-align: center;
  padding: 0 15px;
  white-space: nowrap; */

  width: 75px;
  text-align: center;
  padding: 4px 0;
  font-size: 13px;
  white-space: nowrap;
  border-left: 1px solid #ccc;
  padding: 4px 0;
}
</style>
