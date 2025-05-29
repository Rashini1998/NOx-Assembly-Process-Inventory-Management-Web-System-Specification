<template>
  <div class="chart-container">
    <div class="header-row"
      style="display: flex; justify-content: flex-end; align-items: center; margin-right: 10px; margin-top: 10px; margin-bottom: 10px;">
      <div class="radio-group" style="display: flex; gap: 10px;">
        <label><input type="radio" v-model="selectedTimeUnit" name="option" value="a" /> {{ trend.chartOptions.dailyUnit
        }}</label>
        <label><input type="radio" v-model="selectedTimeUnit" name="option" value="b" /> {{ trend.chartOptions.hourUnit
        }}</label>
      </div>
    </div>
    <!-- Scrollbar container above the chart -->
    <div v-if="selectedTimeUnit === 'b'">
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
    <div v-else class="no-data-message">
      日単位データを表示中 (Showing daily data)
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

const selectedTimeUnit = ref('a'); // 'a' for daily, 'b' for hourly


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

  // Fetch threshold data
  const thresholdData = await fetchThresholdData();

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

  // Calculate max value for y-axis scaling
  const maxDataValue = Math.max(...chartData.datasets[0].data.filter(val => val !== null));
  const upperLimit = thresholdData ? parseFloat(thresholdData['基準在庫上限数']) : 0;
  const yAxisMax = Math.max(maxDataValue * 1.1, upperLimit * 1.1) || 10;


  // Create annotations for the threshold lines
  const annotations = {};

  if (thresholdData) {
    annotations.annotations = {
      upperLimit: {
        type: 'line',
        yMin: parseFloat(thresholdData['基準在庫上限数']),
        yMax: parseFloat(thresholdData['基準在庫上限数']),
        borderColor: '#febf03',
        borderWidth: 2,
        borderDash: [6, 6],
        label: {
          content: `Upper Limit: ${thresholdData['基準在庫上限数']}`,
          enabled: true,
          position: 'right'
        }
      },
      lowerLimit: {
        type: 'line',
        yMin: parseFloat(thresholdData['基準在庫下限数']),
        yMax: parseFloat(thresholdData['基準在庫下限数']),

        borderColor: '#f92020',
        borderWidth: 2,
        borderDash: [6, 6],
        label: {
          content: `Lower Limit: ${thresholdData['基準在庫下限数']}`,
          enabled: true,
          position: 'right'
        }
      },
      standard: {
        type: 'line',
        yMin: parseFloat(thresholdData['基準在庫数']),
        yMax: parseFloat(thresholdData['基準在庫数']),
        borderColor: '#00ae4b',
        borderWidth: 2,
        label: {
          content: `Standard: ${thresholdData['基準在庫数']}`,
          enabled: true,
          position: 'right'
        }
      }
    };
  }

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
          left: 40,
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
              // return `${context.raw}`;
              return Number(context.raw).toFixed(2);
            }
          }
        },
        annotation: annotations
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
          // max: Math.max(...chartData.datasets[0].data.filter(val => val !== null)) * 1.1 || 10,
          max: yAxisMax,
          ticks: {
            precision: 0,
            callback: function (value) {
              if (Number.isInteger(value)) {
                return value;
              }
              // Otherwise show up to 2 decimal places
              return '';
            },
            stepSize: 1,
            // count: Math.ceil(Math.max(...chartData.datasets[0].data.filter(val => val !== null)) * 1.1) || 10
            count: Math.ceil(yAxisMax)
          }
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

const fetchThresholdData = async () => {
  try {
    if (!props.partNumber || !props.process) return null;

    const response = await axios.get('http://localhost:5000/api/nox_assy_inv_mgt_thresh', {
      params: {
        partNumber: props.partNumber,
        process: props.process
      }
    });

    return response.data && response.data.length > 0 ? response.data[0] : null;
  } catch (error) {
    console.error('Error fetching threshold data:', error);
    return null;
  }
};


// watch(() => [
//   props.partNumber,
//   props.process,
//   props.startDate,
//   props.endDate,
//   selectedTimeUnit.value
// ], fetchGraphData, { immediate: true });
watch(() => [
  props.partNumber,
  props.process,
  props.startDate,
  props.endDate,
  selectedTimeUnit.value // Add this to watch list
], () => {
  if (selectedTimeUnit.value === 'b') {
    fetchGraphData();
  } else {
    // Clean up if switching away from hourly view
    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }
    apiData.value = [];
  }
}, { immediate: true });

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
  }
});

// onMounted(() => {
//   fetchGraphData();
// });

onMounted(() => {
  if (selectedTimeUnit.value === 'b') {
    fetchGraphData();
  }
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

const setupXAxisLabels = (labels) => {
  const datesRow = document.querySelector('.dates-row');
  const timesRow = document.querySelector('.times-row');
  const valuesRow = document.querySelector('.values-row');
  if (!datesRow || !timesRow || !valuesRow) return;

  // Clear previous
  datesRow.innerHTML = '';
  timesRow.innerHTML = '';
  valuesRow.innerHTML = '';

  const barWidth = 60;
  const barSpacing = 15;
  const cellWidth = barWidth + barSpacing;

  labels.forEach(([date, time], index) => {
    // Date cell
    const dateCell = document.createElement('td');
    dateCell.className = 'date-label';
    dateCell.style.width = `${cellWidth}px`;
    dateCell.textContent = date;
    datesRow.appendChild(dateCell);

    // Time cell
    const timeCell = document.createElement('td');
    timeCell.className = 'time-label';
    timeCell.style.width = `${cellWidth}px`;
    timeCell.textContent = time;
    timesRow.appendChild(timeCell);


    const valueCell = document.createElement('td');
    valueCell.className = 'value-label';
    valueCell.style.width = `${cellWidth}px`;
    if (apiData.value && apiData.value[index] && apiData.value[index].value !== undefined) {
      valueCell.textContent = Number(apiData.value[index].value).toFixed(0);
    } else {
      valueCell.textContent = '-';
    }
    valuesRow.appendChild(valueCell);
  });

  // Sync scroll
  const syncXAxisLabels = () => {
    const xAxisScroll = document.querySelector('.x-axis-scroll');
    if (xAxisScroll && scrollContainer.value) {
      xAxisScroll.scrollLeft = scrollContainer.value.scrollLeft;
    }
  };

  scrollContainer.value.addEventListener('scroll', syncXAxisLabels);
};


const exportToCSV = () => {
  if (!apiData.value || apiData.value.length === 0) {
    alert('No data available to export');
    return;
  }

  // Prepare CSV header
  const headers = ['Date', 'Time', 'Value'];
  
  // Prepare CSV rows
  const rows = apiData.value.map(item => {
    const date = format(parseISO(item.timestamp), 'MM/dd');
    const time = format(parseISO(item.timestamp), 'H:mm');
    const value = item.value !== null ? item.value.toFixed(0) : '-';
    return [date, time, value];
  });

  // Combine header and rows
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n');

  // Create download link
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `inventory_data_${props.partNumber}_${format(new Date(), 'yyyyMMdd')}.csv`);
  link.style.visibility = 'hidden';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

// Expose the export function to parent component
defineExpose({
  exportToCSV
});

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
  overflow-x: hidden;
  flex: 1;
}

.labels-table {
  border-collapse: collapse;
  table-layout: fixed;
  display: block;
  width: max-content;
}

.labels-table-new {
  border-bottom: #1c0808;
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
  display: inline-block;
}

.labels-table {
  display: block;
  width: max-content;
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

.process-label {
  text-align: center;
  font-size: 12px;
  color: #333;
}

.value-label {
  text-align: center;
  font-weight: bold !;
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
  /* background-color: #808080; */
  /* border-top: 2px solid #808080; */
  /* border-bottom: 2px solid #aaa; */
  font-size: 14px;
}

.x-axis-labels-container::-webkit-scrollbar {
  display: none;
  /* Hide scrollbar for Chrome/Safari */
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
  ;
}

.nameLable {
  background-color: #808080;
  margin-bottom: 13px;
}

.valueLabel {
  background-color: #d4d4d4 !important;
}

.assy-info-new {
  background-color: #dcdcdc;
  border-color: #808080;
  font-size: 10px;

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

.date-label,
.time-label {
  width: 75px;
  text-align: center;
  padding: 4px 0;
  font-size: 13px;
  white-space: nowrap;
  border-left: 1px solid #ccc;
  padding: 4px 0;
}
</style>