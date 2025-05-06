<template>
    <header>
        <div class="min-h-screen ">
    <div class="bg-black shadow-md py-4 px-6">
      <TitleBar :updatedTime="lastUpdated" @refresh="manualRefresh"/>
    </div>
    <h1 class="text-gray-100">
      Hello Capacity Page
    </h1>

  </div>
    </header>

</template>
<script setup>
import {ref,onMounted, onBeforeUnmount} from 'vue';
import TitleBar from '@/components/TitleBar.vue';
import axios from 'axios';

const tableData = ref([]);
const lastUpdated = ref('');
const refreshInterval = ref(60000);
let intervalId = null;

//Fetch data from API
const fetchInventoryAvailableData = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/inventory-availability')
    tableData.value = response.data;
    lastUpdated.value = new Date().toLocaleString();

  } catch (error) {
    console.error("Error fetching inventory history", error);
  }
}

//Get refresh interval from backend
const fetchRefreshInterval = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/refresh-config');
    refreshInterval.value = res.data.refresh_interval * 60 * 1000; // convert to ms
  } catch (e) {
    console.warn('Failed to load refresh interval, using default.');
  }
};

// Setup automatic refresh
const setupAutoRefresh = () => {
  clearInterval(intervalId);
  intervalId = setInterval(() => {
    fetchInventoryAvailableData();
  }, refreshInterval.value);
};

onMounted(async () => {
  await fetchRefreshInterval();
  await fetchInventoryAvailableData();
  setupAutoRefresh();
});

onBeforeUnmount(() => {
  clearInterval(intervalId);
});

// Manual Refresh
const manualRefresh = () => {
  fetchInventoryAvailableData();
};
</script>