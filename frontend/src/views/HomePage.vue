<template>
  <!-- <div class="bg-gray-100 min-h-screen pt-20"> -->
  <div class="min-h-screen">
    <div class="bg-black shadow-md py-4 px-4">
      <TitleBar :updatedTime="lastUpdated" @refresh="manualRefresh" />
    </div>

    <!-- Filter/Search Bar -->
    <div class="bg-black shadow-md">
      <!-- <FilterBar @search="handleSearch" @export="handleExport" /> -->
      <FilterBar @search="handleSearch" @export="exportToCSV" @update-manufacturer="selectedManufacturer = $event"
        @update-product-number="selectedProductNumber = $event" @update-classification="selectedClassification = $event"
        :manufacturers="uniqueManufacturers" :productNumbers="uniqueProductNumbers"
        :classifications="uniqueClassifications" />

    </div>

    <!-- Inventory Table Section -->
    <div class="overflow-x-auto p-4">
      <InventoryTable :data="filteredData" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';
// import jsPDF from 'jspdf'
// import autoTable from 'jspdf-autotable'
import FilterBar from '@/components/FilterBar.vue'
import InventoryTable from '@/components/InventoryTable.vue'
import TitleBar from '@/components/TitleBar.vue'

const tableData = ref([]);
const query = ref('');
const lastUpdated = ref('');
const refreshInterval = ref(60000);
let intervalId = null;

const selectedManufacturer = ref('')
const selectedProductNumber = ref('')
const selectedClassification = ref('')

const uniqueManufacturers = computed(() => [...new Set(tableData.value.map(item => item.manufacturer))])
const uniqueProductNumbers = computed(() => [...new Set(tableData.value.map(item => item.assyNumber))])
const uniqueClassifications = computed(() => [...new Set(tableData.value.map(item => item.classification))])


//Fetch data from API
const fetchInventoryData = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/inventory-history')
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
    fetchInventoryData();
  }, refreshInterval.value);
};

//Fetch on page load
// onMounted(() => {
//   fetchInventoryData()
// })
onMounted(async () => {
  await fetchRefreshInterval();
  await fetchInventoryData();
  setupAutoRefresh();
});

onBeforeUnmount(() => {
  clearInterval(intervalId);
});

//Search filter
const handleSearch = (val) => {
  query.value = val.toLowerCase()
}
const filteredData = computed(() => {
  return tableData.value.filter((item) => {
    const matchesSearch = Object.values(item).some((v) =>
      String(v).toLowerCase().includes(query.value)
    );
    const matchesManufacturer = selectedManufacturer.value ? item.manufacturer === selectedManufacturer.value : true;
    const matchesProduct = selectedProductNumber.value ? item.assyNumber === selectedProductNumber.value : true;
    const matchesClassification = selectedClassification.value ? item.classification === selectedClassification.value : true;

    return matchesSearch && matchesManufacturer && matchesProduct && matchesClassification;
  });
});


// Manual Refresh
const manualRefresh = () => {
  fetchInventoryData();
};

// export to pdf
// const handleExport = () => {
//   const doc = new jsPDF()
//   autoTable(doc, {
//     head: [['Manufacturer', 'ASSY', 'SUBASSY', 'Shipping', 'Air', 'SCU', 'Vapor', 'Char.', 'Frac.', 'Acc.', 'FA', 'FA Frac.', 'Visual', 'Total']],
//     body: filteredData.value.map(item => [
//       item.manufacturer,
//       item.assy,
//       item.subassy,
//       item.shipping,
//       item.air,
//       item.scu,
//       item.vapor,
//       item.characteristic,
//       item.fractional,
//       item.accessories,
//       item.fa,
//       item.faFractional,
//       item.visual,
//       item.total
//     ])
//   })
//   doc.save('inventory_export.pdf')
// }

// export to csv
function exportToCSV() {
  const headers = [
    "Manufacturer", "Assy", "Sub Assy", "Classification", "Airtightness", "SCU", "Water Vapor",
    "Characteristic", "Fractional", "Accessories", "FA", "FA Fractional",
    "Visual", "Total"
  ]

  // Add the 'total' value for each row using the computed total
  const rows = tableData.value.map(item => {
    const total = [
      'airtightness', 'scu', 'waterVapor',
      'inspection', 'fractional', 'accessories', 'fa',
      'faFractional', 'visual'
    ].reduce((sum, key) => sum + Number(item[key] || 0), 0)

    return [
      item.manufacturer,
      item.assyNumber,
      item.subassyNumber,
      item.classification,
      item.airtightness,
      item.scu,
      item.waterVapor,
      item.inspection,
      item.fractional,
      item.accessories,
      item.fa,
      item.faFractional,
      item.visual,
      total // Include the computed total here
    ];
  });
  const csvContent = [headers, ...rows]
    .map(e => e.join(","))
    .join("\n");

  const bom = "\uFEFF";
  // const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" })
  const blob = new Blob([bom + csvContent], { type: "text/csv;charset=utf-8;" });

  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.setAttribute("href", url)
  link.setAttribute("download", "inventory.csv")
  link.click();
}
</script>