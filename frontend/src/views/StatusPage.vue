<template>
  <header>
    <div class=" min-h-screen ">
      <div class="bg-black shadow-md py-4 px-6">
        <TitleBar :updatedTime="lastUpdated" @refresh="manualRefresh" />
      </div>
      <!-- Filter/Search Bar -->
      <div class="bg-black shadow-md">
        <StatusFilterBar @search="handleSearch" @export="exportToCSV" @update-tagId="selectedtagId = $event"
          @update-nextProcessName="selectednextProcessName = $event" @update-workStatus="selectedworkStatus = $event"
          @update-partNumber="selectedpartNumber = $event" 
          :tagIds="uniquetagIds"
          :nextProcessNames="uniquenextProcessNames" :workStatuses="uniqueworkStatuses"
          :partNumbers="uniquepartNumbers" />
      </div>

      <!-- Inventory Table Section -->
      <div class="overflow-x-auto p-4">
        <StatusTable :data="filteredData" />
      </div>
    </div>
  </header>

</template>
<script setup>

import StatusFilterBar from '@/components/StatusFilterBar.vue';
import TitleBar from '@/components/TitleBar.vue'
import { ref, computed, onMounted, onBeforeUnmount  } from 'vue';
import axios from 'axios';
import StatusTable from '@/components/StatusTable.vue';

const tableData = ref([]);
const query = ref('');
const lastUpdated = ref('');
const refreshInterval = ref(60000);
let intervalId = null;

// tableData=[
// {
//     "DurationOfStay": ,
//     "NextProcessName": "",
//     "PartNumber": "",
//     "ProcessingLot": "",
//     "Quantity": ,
//     "ShelfTagID": "",
//     "ShelfTagRegistrationDate": "",
//     "ShelfTagUpdateDate": "",
//     "WorkStatus":
//   },
// ]



// Filter Inputs (from StatusFilterBar)-->hold the current user-selected filters
const selectedtagId = ref('')
const selectednextProcessName = ref('')
const selectedworkStatus = ref('')
const selectedpartNumber = ref('')

const uniquetagIds = computed(() => [...new Set(tableData.value.map(item => item.ShelfTagID))])
const uniquenextProcessNames = computed(() => [...new Set(tableData.value.map(item => item.NextProcessName))])
const uniqueworkStatuses = computed(() => [...new Set(tableData.value.map(item => item.WorkStatus))])
const uniquepartNumbers = computed(() => [...new Set(tableData.value.map(item => item.PartNumber))])

//Fetch data from API
const fetchStatusData = async () => {
  try {
    const response = await axios.get('http://localhost:5000/api/label-status')
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
    fetchStatusData();
  }, refreshInterval.value);
};

//Fetch on page load
onMounted( async() => {
  await fetchRefreshInterval();
  await fetchStatusData();
  setupAutoRefresh();

  // fetchStatusData()
})

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
    const matchesTagId = selectedtagId.value ? item.ShelfTagID === selectedtagId.value : true;
    const matchesNextProcessName = selectednextProcessName.value ? item.NextProcessName === selectednextProcessName.value : true;
    const matchesWorkStatus = selectedworkStatus.value ? item.WorkStatus === selectedworkStatus.value : true;
    const matchesPartNumber = selectedpartNumber.value ? item.PartNumber === selectedpartNumber.value : true;

    return matchesSearch && matchesTagId && matchesNextProcessName && matchesWorkStatus && matchesPartNumber;
  });
});

// export to csv
function exportToCSV(){
  const headers = [
    "棚札ID","品番", "次工程名称", "加工Lot", "数量", "作業状況", "棚札登録日時", "棚札更新日時", "滞留日数"
  ]

  const rows = tableData.value.map(item =>{
    return[
      item.ShelfTagID,
      item.PartNumber,
      item.NextProcessName,
      item.ProcessingLot,
      item.Quantity,
      item.WorkStatus,
      item.ShelfTagRegistrationDate,
      item.ShelfTagUpdateDate,
      item.DurationOfStay
    ];
  });

  const csvContent = [headers, ...rows]
  .map(e=>e.join(',')).join("\n");

  const bom = "\uFEFF";
  // const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" })
  const blob = new Blob([bom + csvContent], { type: "text/csv;charset=utf-8;" });
  
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.setAttribute("href", url)
  link.setAttribute("download", "inventory.csv")
  link.click();

}

// Manual Refresh
const manualRefresh = () => {
  fetchStatusData();
};

</script>
