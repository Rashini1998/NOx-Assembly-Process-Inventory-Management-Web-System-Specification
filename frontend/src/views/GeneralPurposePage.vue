<template>
  <header>
    <div class="min-h-screen">
      <div class="bg-black shadow-md py-4 px-6 flex items-center text-white space-x-3">
        <div class="font-semibold text-xl">{{ home.title }}</div>
        <select v-model="selectedTable" @change="fetchTableData"
          class=" text-white font-semibold  px-2 py-1 rounded" :style="{ backgroundColor: pickedColor }">
          <option value="" disabled selected>{{ home.selection.select }}</option>
          <option value="inventory_history">{{ home.title }}-{{ home.selection.page01 }}</option>
          <option value="realtime_shelf_label_status">{{ home.title }}-{{ home.selection.page02 }}</option>
        </select>
      </div>
      <div class="bg-black shadow-md py-4 px-3 flex items-center text-white space-x-3">
        <div>{{ home.database }} : {{ home.test }}</div>
        <div>{{ home.table }} : {{ dynamicTableName }}</div>
        <TitleBar :updatedTime="lastUpdated" @refresh="manualRefresh" />
      </div>

      <div class="p-6">
        <div v-if="loading" class="text-center py-8">
          Loading...
        </div>

        <div v-else-if="error" class="text-red-500 p-4 bg-red-100 rounded">
          {{ error }}
        </div>

        <div v-else-if="tableData.columns && tableData.columns.length" class="overflow-x-auto">
          <table class="min-w-full bg-white border border-gray-300 text-center" style="background-color:rgb(212 212 212);">
            <thead>
              <tr>
                <th v-for="(column, index) in tableData.columns" :key="column"
                  class="py-2 px-4 border-b border-gray-300 text-center text-sm" 
                  :class="{ 'border-r border-white': index < tableData.columns.length - 1 }" 
                  style="background-color: rgba(128,128,128,255);">
                  {{ formatHeader(column) }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, rowIndex) in tableData.data" :key="rowIndex">
                <td v-for="(column, colIndex) in tableData.columns" :key="column" class="py-2 px-4 border-b border-white" 
                :class="{ 'border-r border-gray-300': colIndex < tableData.columns.length - 1 }"
                style="background-color:rgb(212 212 212);">
                  {{ row[column] }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-8 text-gray-500">
          <!-- Select a screen from the dropdown to view data -->
           データを表示するには、ドロップダウンから画面を選択します。
        </div>
      </div>
    </div>

  </header>

</template>
<script setup>
import { ref, computed,onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios';
import TitleBar from '@/components/TitleBar.vue'
import generalData from '@/assets/config/general.yaml'

const home = ref(generalData.general)
const pickedColor = ref('#212121')
const selectedTable = ref('')
const tableData = ref({ columns: [], data: [] })
const loading = ref(false)
const error = ref(null)
const lastUpdated = ref('');
const refreshInterval = ref(60000);
let intervalId = null;


// Computed property to dynamically determine the table name
const dynamicTableName = computed(() => {
  if (selectedTable.value === 'inventory_history') {
    return 'nox_assy_wip_inventories_new';
  } else if (selectedTable.value === 'realtime_shelf_label_status') {
    return 'nox_assy_esl_status';
  } else {
    return 'N/A'; // Or a default placeholder if no table is selected
  }
});
const fetchTableData = async () => {
  if (!selectedTable.value) {
    tableData.value = { columns: [], data: [] }
    return
  }

  loading.value = true
  error.value = null

  try {
    const response = await fetch(`http://localhost:5000/api/dynamic-table?table=${selectedTable.value}`)
    if (!response.ok) {
      throw new Error('Failed to fetch table data')
    }
    tableData.value = await response.json()
    lastUpdated.value = new Date().toLocaleString();
  } catch (err) {
    error.value = err.message
    tableData.value = { columns: [], data: [] }
    lastUpdated.value = 'Failed to load';
  } finally {
    loading.value = false
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
    fetchTableData();
  }, refreshInterval.value);
};

const formatHeader = (header) => {
  // Convert snake_case or CamelCase to readable format
  return header
    .replace(/_/g, ' ')
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
}
//Fetch on page load
onMounted(async () => {
  await fetchRefreshInterval();
  await fetchTableData();
  setupAutoRefresh();

  // fetchStatusData()
})

onBeforeUnmount(() => {
  clearInterval(intervalId);
});

// Manual Refresh
const manualRefresh = () => {
  fetchTableData();
};
</script>



<style scoped>
table {
  border-collapse: collapse;
}

th,
td {
  padding: 8px 12px;
  text-align: left;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f0f0f0;
}
</style>