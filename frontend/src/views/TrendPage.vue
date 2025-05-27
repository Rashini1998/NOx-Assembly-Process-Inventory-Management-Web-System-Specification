<template>
  <header>
    <div class="min-h-screen">
      <div class="bg-black shadow-md py-4 px-6">
        <TitleBar :updatedTime="lastUpdated" @refresh="manualRefresh" />
      </div>
      <div>
        <TrendFilter 
          @search="handleSearch" 
          @export="exportToCSV" 
          @update-partNumber="selectedPartNumber = $event"
          @update-startDate="selectedStartDate = $event" 
          @update-endDate="selectedEndDate = $event"
          @update-process="selectedProcess = $event" 
          :partNumbers="uniquepartNumbers" 
          :processes="uniqueProcesses" 
        />
        <InventoryGraph
          :partNumber="selectedPartNumber"
          :process="selectedProcess"
          :startDate="selectedStartDate"
          :endDate="selectedEndDate"
        />
      </div>
    </div>
  </header>
</template>

<script setup>
import TitleBar from '@/components/TitleBar.vue'
import TrendFilter from '@/components/TrendFilter.vue'
import InventoryGraph from '@/components/InventoryGraph.vue';
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';

const tableData = ref([]);
const lastUpdated = ref('');
const refreshInterval = ref(60000);
let intervalId = null;

const selectedPartNumber = ref('');
const selectedStartDate = ref(null);
const selectedEndDate = ref(null);
const selectedProcess = ref('');
// const selectedPartNumber = ref('1144780280');
// const selectedStartDate = ref('2024/09/24');
// const selectedEndDate = ref('2024/09/24');
// const selectedProcess = ref('FA');


const uniquepartNumbers = computed(() => [...new Set(tableData.value.map(item => item.ASSY品番))]);
const uniqueProcesses = computed(() => {
  return [...new Set(tableData.value.map(item => item.在庫管理グループ名称).filter(Boolean))];
});

const fetchInventoriesData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/iitsMaster');
    tableData.value = response.data;
    lastUpdated.value = new Date().toLocaleString();
  } catch (error) {
    console.error("Error fetching inventory history", error);
  }
};

const fetchRefreshInterval = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/refresh-config');
    refreshInterval.value = res.data.refresh_interval * 60 * 1000;
  } catch (e) {
    console.warn('Failed to load refresh interval, using default.');
  }
};

const setupAutoRefresh = () => {
  clearInterval(intervalId);
  intervalId = setInterval(() => {
    fetchInventoriesData();
  }, refreshInterval.value);
};

const handleSearch = () => {
  // The actual filtering is now handled by InventoryGraph via its props
  console.log("Search triggered with:", {
    partNumber: selectedPartNumber.value,
    process: selectedProcess.value,
    startDate: selectedStartDate.value,
    endDate: selectedEndDate.value
  });
};

const manualRefresh = () => {
  fetchInventoriesData();
};

const exportToCSV = () => {
  // Implement your CSV export logic here
  console.log("Export to CSV");
};

onMounted(async () => {
  await fetchRefreshInterval();
  await fetchInventoriesData();
  setupAutoRefresh();
});

onBeforeUnmount(() => {
  clearInterval(intervalId);
});
</script>