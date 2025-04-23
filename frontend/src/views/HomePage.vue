<template>
  <div class="bg-gray-100 min-h-screen pt-20">
    <div class="bg-black shadow-md py-4 px-6">
      <TitleBar />
    </div>

    <!-- Filter/Search Bar -->
    <div class="bg-black shadow-md py-4 px-6">
      <!-- <FilterBar @search="handleSearch" @export="handleExport" /> -->
      <FilterBar @search="handleSearch" @export="exportToCSV" />

    </div>

    <!-- Inventory Table Section -->
    <div class="overflow-x-auto p-4">
      <InventoryTable :data="filteredData" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
// import jsPDF from 'jspdf'
// import autoTable from 'jspdf-autotable'
import FilterBar from '@/components/FilterBar.vue'
import InventoryTable from '@/components/InventoryTable.vue'
import TitleBar from '@/components/TitleBar.vue'

// Dummy data for now (replace with real API or prop later)
// const tableData = ref([
//   {
//     manufacturer: 'GUSTO',
//     assyNumber: 1144780012,
//     subassyNumber: '4486000012',
//     classification: '国内・市販',
//     airtightness: 0,
//     scu: 0,
//     waterVapor: 0,
//     inspection: 0,
//     fractional: 0,
//     accessories: 2,
//     fa: 13,
//     faFractional: 0,
//     visual: 1,
//   },
//   {
//     manufacturer: 'BAMIYAN',
//     assyNumber: 1144780200,
//     subassyNumber: '4486000200',
//     classification: '国内',
//     airtightness: 0,
//     scu: 0,
//     waterVapor: 0,
//     inspection: 153,
//     fractional: 8,
//     accessories: 0,
//     fa: 29,
//     faFractional: 18,
//     visual: 59,
//   },
//   {
//     manufacturer: 'SYABUYO',
//     assyNumber: 1144785220,
//     subassyNumber: '4486005220',
//     classification: '海外',
//     airtightness: 30,
//     scu: 0,
//     waterVapor: 0,
//     inspection: 0,
//     fractional: 0,
//     accessories: 0,
//     fa: 0,
//     faFractional: 1,
//     visual: 0,
//   },

// ])

const tableData = ref([]);
const query = ref('')

//Fetch data from API
const fetchInventoryData = async()=>{
  try {
    const response = await axios.get('http://localhost:5000/api/inventory-history')
    tableData.value = response.data
    
  } catch (error) {
    console.error("Error fetching inventory history",error);
  }
}

//Fetch on page load
onMounted(()=>{
  fetchInventoryData()
})

//Search filter
const handleSearch = (val) => {
  query.value = val.toLowerCase()
}
const filteredData = computed(() => {
  return tableData.value.filter((item) =>
    Object.values(item).some((v) => String(v).toLowerCase().includes(query.value))
  )
})

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