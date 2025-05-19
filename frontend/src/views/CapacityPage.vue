<template>
  <header>
    <div class="min-h-screen ">
      <div class="bg-black shadow-md py-4 px-6">
        <TitleBar :updatedTime="lastUpdated" @refresh="manualRefresh" />
      </div>

      <div class="bg-black shadow-md">
        <!-- <FilterBar @search="handleSearch" @export="handleExport" /> -->
        <ProcessRange @update-process-range= "updateProcessRange" />
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

const allData = ref([])

const selectedPartNumber = ref('')
const selectedShipment = ref('')
const selectedManufacturer = ref('')

const uniquePartNumbers = computed(() => [...new Set(tableData.value.map(item => item.ProductNumber))])
const uniqueShipments = computed(() => [...new Set(tableData.value.map(item => item.ShippingClassification))])
const uniqueManufacturers = computed(() => [...new Set(tableData.value.map(item => item.Manufacturer))])

const selectedProcessRange = ref({start: '', end: ''});

//Fetch data from API
const fetchInventoryAvailableData = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/inventory-availability')
    tableData.value = response.data;
    allData.value=response.data;
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

const processKeyMap = {
  airtight_inspection: 'AirtightnessInspection',
  scu: 'SCU',
  water_vapor_inspection: 'WaterVaporInspection',
  characteristics_inspection: 'CharacteristicInspection',
  characteristics_inspection_odd: 'CharacteristicInspectionOddLot',
  accessories: 'Accessories',
  fa: 'FA',
  fa_fractional: 'FAFractionalItems',
  visual_inspection: 'VisualInspection',
};

const processOrder = [
  'AirtightnessInspection',
  'SCU',
  'WaterVaporInspection',
  'CharacteristicInspection',
  'CharacteristicInspectionOddLot',
  'Accessories',
  'FA',
  'FAFractionalItems',
  'VisualInspection'
];

const updateProcessRange = ({ start, end }) => {
  const mappedStart = processKeyMap[start];
  const mappedEnd = processKeyMap[end];

  selectedProcessRange.value = { start: mappedStart, end: mappedEnd };

  if (!mappedStart || !mappedEnd) {
    tableData.value = allData.value;
    return;
  }

  const startIdx = processOrder.indexOf(start);
  const endIdx = processOrder.indexOf(end);

  if (startIdx === -1 || endIdx === -1 || startIdx > endIdx) {
    tableData.value = allData.value;
    return;
  }

  const filtered = allData.value.filter(item => {
    const processIdx = processOrder.indexOf(item.ProcessName);
    return processIdx >= startIdx && processIdx <= endIdx;
  });

  tableData.value = filtered;
};

const filteredData = computed(() => {
  return tableData.value.filter((item) => {
    const matchesSearch = Object.values(item).some((v) =>
      String(v).toLowerCase().includes(query.value)
    );
    const matchesPartNumber = selectedPartNumber.value ? item.ProductNumber === selectedPartNumber.value : true;
    const matchesShipment = selectedShipment.value ? item.ShippingClassification === selectedShipment.value : true;
    const matchesManufacturer= selectedManufacturer.value ? item.Manufacturer === selectedManufacturer.value : true;

    return matchesPartNumber && matchesShipment && matchesManufacturer && matchesSearch;
  })
  .map((item)=>{
    const start = selectedProcessRange.value?.start;
    const end = selectedProcessRange.value?.end;

    const startIndex  = processOrder.indexOf(start);
    const endIndex = processOrder.indexOf(end);
    if(
      startIndex !== -1 &&
      endIndex !== -1 &&
      startIndex <= endIndex
    ){
      const keysToSum = processOrder.slice(startIndex, endIndex + 1);
      const total = keysToSum.reduce((sum, key) => {
          const value = Number(item[key]);
          return sum + (isNaN(value) ? 0 : value);
        }, 0);
        return {...item, inProcessInventory: total};
    }
    return {...item, inProcessInventory:0};
  });
});



//export to csv

// function exportToCSV() {
//   const headers = [
//     "Manufacturer", "Assy", "Sub Assy", "Classification", "Airtightness", "SCU", "Water Vapor",
//     "Characteristic", "Fractional", "Accessories", "FA", "FA Fractional",
//     "Visual", "Total"
//   ]

//   // Add the 'total' value for each row using the computed total
//   const rows = tableData.value.map(item => {
//     const total = [
//       'airtightness', 'scu', 'waterVapor',
//       'inspection', 'fractional', 'accessories', 'fa',
//       'faFractional', 'visual'
//     ].reduce((sum, key) => sum + Number(item[key] || 0), 0)

//     return [
//       item.manufacturer,
//       item.assyNumber,
//       item.subassyNumber,
//       item.classification,
//       item.airtightness,
//       item.scu,
//       item.waterVapor,
//       item.inspection,
//       item.fractional,
//       item.accessories,
//       item.fa,
//       item.faFractional,
//       item.visual,
//       total // Include the computed total here
//     ];
//   });
//   const csvContent = [headers, ...rows]
//     .map(e => e.join(","))
//     .join("\n");

//   const bom = "\uFEFF";
//   // const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" })
//   const blob = new Blob([bom + csvContent], { type: "text/csv;charset=utf-8;" });

//   const url = URL.createObjectURL(blob)
//   const link = document.createElement("a")
//   link.setAttribute("href", url)
//   link.setAttribute("download", "inventory.csv")
//   link.click();
// }

</script>