<template>
  <header>
    <div class="min-h-screen ">
      <div class="bg-black shadow-md py-4 px-6">
        <TitleBar :updatedTime="lastUpdated" @refresh="manualRefresh" />
      </div>

      <div class="bg-black shadow-md">
        <!-- <FilterBar @search="handleSearch" @export="handleExport" /> -->
        <ProcessRange />
      </div>

      <!-- Filter/Search Bar -->
      <div class="bg-black shadow-md">
        <!-- <FilterBar @search="handleSearch" @export="handleExport" /> -->
        <CapacityFilterBar @search="handleSearch" @export="exportToCSV" @update-partNumber="selectedPartNumber = $event"
        @update-shipment="selectedShipment = $event" @update-manufacturer="selectedManufacturer = $event"
        :partNumbers="uniquePartNumbers" :shipments="uniqueShipments"
        :manufacturers="uniqueManufacturers" />
      </div>

          <!-- Inventory Table Section -->
    <div class="overflow-x-auto p-4">
      <CapacityTable :data="filteredData" />
    </div>

    </div>
  </header>

</template>
<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import TitleBar from '@/components/TitleBar.vue';
import axios from 'axios';
import ProcessRange from '@/components/ProcessRange.vue';
import CapacityFilterBar from '@/components/CapacityFilterBar.vue';
import CapacityTable from '@/components/CapacityTable.vue';

const tableData = ref([]);
const lastUpdated = ref('');
const refreshInterval = ref(60000);
let intervalId = null;
const query = ref('');

const selectedPartNumber = ref('')
const selectedShipment = ref('')
const selectedManufacturer = ref('')

const uniquePartNumbers = computed(() => [...new Set(tableData.value.map(item => item.ProductNumber))])
const uniqueShipments = computed(() => [...new Set(tableData.value.map(item => item.ShippingClassification))])
const uniqueManufacturers = computed(() => [...new Set(tableData.value.map(item => item.Manufacturer))])


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

//Search filter
const handleSearch = (val) => {
  query.value = val.toLowerCase()
}

const filteredData = computed(() => {
  return tableData.value.filter((item) => {
    const matchesSearch = Object.values(item).some((v) =>
      String(v).toLowerCase().includes(query.value)
    );
    const matchesPartNumber = selectedPartNumber.value ? item.ProductNumber === selectedPartNumber.value : true;
    const matchesShipment = selectedShipment.value ? item.ShippingClassification === selectedShipment.value : true;
    const matchesManufacturer= selectedManufacturer.value ? item.Manufacturer === selectedManufacturer.value : true;

    return matchesPartNumber && matchesShipment && matchesManufacturer && matchesSearch;
  });
});

</script>