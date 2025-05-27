
<template>
  <div class="chart-container">
    <div class="chart-wrapper" ref="chartWrapper">
      <div class="scroll-container" ref="scrollContainer">
        <canvas ref="chartCanvas"></canvas>
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
    return {
      labels: [],
      datasets: []
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
      labels.push(format(date, 'MM/dd HH:mm'));
      values.push(item.value);
    }
  });

  return {
    labels,
    datasets: [{
      label: `${props.partNumber} - ${props.process}`,
      data: values,
      backgroundColor: 'red',
      borderColor: 'red',
      borderWidth: 1
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
  if (!apiData.value || apiData.value.length === 0 || !chartCanvas.value) {
    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }
    return;
  }

  const chartData = processApiData(apiData.value);
  
  await nextTick();

  if (chartInstance) {
    chartInstance.destroy();
  }

  const ctx = chartCanvas.value.getContext('2d');
  const dataLength = chartData.labels.length;
  
  const canvasWidth = calculateCanvasWidth(dataLength);
  chartCanvas.value.style.width = `${canvasWidth}px`;
  chartCanvas.value.style.height = '500px';
  chartCanvas.value.width = canvasWidth;
  chartCanvas.value.height = 500;

  // Custom plugin for small black circles on top of bars
  const circleMarkerPlugin = {
    id: 'circleMarker',
    afterDraw(chart) {
      const { ctx, data, scales: { x, y } } = chart;
      
      ctx.save();
      
      data.datasets.forEach((dataset) => {
        dataset.data.forEach((value, index) => {
          if (value > 0) {
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
    plugins: [circleMarkerPlugin],
    options: {
      responsive: false,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: 'top'
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              return `${context.dataset.label}: ${context.raw}`;
            }
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            // text: '在庫量 (Inventory)'
          }
        },
        x: {
          title: {
            display: true,
            // text: '日時 (Date & Time)'
          },
          ticks: {
            autoSkip: false,
            maxRotation: 90,
            minRotation: 90
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
</script>

<style scoped>
/* Keep your existing styles */
.chart-container {
  position: relative;
  width: 100%;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  margin-top: 20px;
  font-family: 'Noto Sans JP', sans-serif;
}

.chart-wrapper {
  width: 100%;
  overflow-x: auto;
  border: 1px solid #eee;
  border-radius: 4px;
  background: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.scroll-container {
  height: 500px;
  min-width: 100%;
  position: relative;
}

.no-data-message {
  padding: 40px;
  text-align: center;
  color: #999;
  font-size: 1.1rem;
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
</style>