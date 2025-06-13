<template>
  <header>
    <div class="min-h-screen bg-black">
      <!-- Title Bar -->
      <div class="bg-black shadow-md py-4 px-6 flex items-center text-white space-x-3">
        <div class="font-semibold text-xl">{{ home.filter.title }}</div>
      </div>

      <!-- Controls -->
      <div class="bg-black shadow-md py-3 px-4 flex items-center text-white space-x-3">
        <div>{{ home.database }} : {{ home.test }}</div>
        <div>{{ home.table }} : nox_assy_inv_mgt_master</div>
        <button @click="openModal"
          class="flex items-center space-x-2 bg-zinc-800 hover:bg-zinc-700 text-white px-3 py-1 rounded ">
          <PlusIcon class="h-5 w-5 text-white" />
          <span>{{ home.filter.addRow }}</span>
        </button>
      </div>

      <!-- Table -->
      <div class="p-5 overflow-x-auto">
        <table class="min-w-full bg-white border">
          <thead>
            <tr class="text-left text-sm font-semibold" style="background-color: rgba(128,128,128,255);">
              <th class="p-2 border text-center">
                <input type="checkbox" @change="toggleAll" />
              </th>

              <th class="p-2 border text-center">{{ home.tableHeaders.No }}</th>
              <th class="p-2 border text-center">{{ home.tableHeaders.EquipmentGroupID }}</th>
              <th class="p-2 border text-center">{{ home.tableHeaders.EquipmentSerialNumber }}</th>
              <th class="p-2 border text-center">{{ home.tableHeaders.EquipmentGroupName }}</th>
              <th class="p-2 border text-center">{{ home.tableHeaders.InventoryManagementGroupID }}</th>
              <th class="p-2 border text-center">{{ home.tableHeaders.InventoryManagementGroupName }}</th>
              <th class="p-2 border text-center">{{ home.tableHeaders.StandardInventoryDays }}</th>
              <th class="p-2 border text-center">{{ home.tableHeaders.StandardInventoryManagementRang }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in tableData" :key="row.設備機番" class="text-sm" style="background-color:rgb(212 212 212);">
              <td class="p-2 border text-center">
                <input type="checkbox" v-model="selectedRows" :value="row.id" />
              </td>

              <td class="p-2 border text-right">{{ row.id }}</td>
              <td class="p-2 border text-right">{{ row.設備グループID }}</td>
              <td class="p-2 border text-right">{{ row.設備機番 }}</td>
              <td class="p-2 border text-right">{{ row.設備グループ名称 }}</td>
              <td class="p-2 border text-right">{{ row.在庫管理グループID }}</td>
              <td class="p-2 border text-right">{{ row.在庫管理グループ名称 }}</td>
              <td class="p-2 border text-right">{{ row.基準在庫日数 }}</td>
              <td class="p-2 border text-right">{{ row.基準在庫管理幅 }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Modal -->
      <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div class="bg-zinc-900 text-white p-6 rounded-lg w-[500px] space-y-4 shadow-lg">
          <div class="flex items-center space-x-2 border-b border-zinc-700 pb-2">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M5.121 17.804A13.937 13.937 0 0112 15c2.558 0 4.943.768 6.879 2.086M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <h2 class="text-lg font-semibold">{{ home.modal.addRow }}</h2>
          </div>

          <div class="grid grid-cols-2 gap-4">
            <input v-model="newRow.設備グループID" placeholder="設備グループID"
              class="bg-zinc-800 text-white border border-zinc-600 p-2 rounded" />
            <input v-model="newRow.設備グループ名称" placeholder="設備グループ名称"
              class="bg-zinc-800 text-white border border-zinc-600 p-2 rounded" />

            <input v-model="newRow.在庫管理グループID" placeholder="在庫管理グループID"
              class="bg-zinc-800 text-white border border-zinc-600 p-2 rounded" />
            <input v-model="newRow.在庫管理グループ名称" placeholder="在庫管理グループ名称"
              class="bg-zinc-800 text-white border border-zinc-600 p-2 rounded" />

            <input v-model="newRow.設備機番" placeholder="設備機番*"
              class="bg-zinc-800 text-white border border-zinc-600 p-2 rounded col-span-1" />
            <input v-model="newRow.基準在庫日数" type="number" placeholder="基準在庫日数*"
              class="bg-zinc-800 text-white border border-zinc-600 p-2 rounded col-span-1" />
            <input v-model="newRow.基準在庫管理幅" placeholder="基準在庫管理幅"
              class="bg-zinc-800 text-white border border-zinc-600 p-2 rounded col-span-2" />
          </div>

          <div class="flex justify-end border-t border-zinc-700 pt-4 space-x-2">
            <button @click="closeModal" class="px-4 py-1 rounded bg-zinc-700 hover:bg-zinc-600">キャンセル</button>
            <button @click="addRow"
              class="px-4 py-1 rounded bg-blue-900 hover:bg-blue-600 text-white transition-colors">追加</button>
          </div>
        </div>
      </div>

    </div>
  </header>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { PlusIcon } from '@heroicons/vue/24/solid'
import axios from 'axios'
import settingData from '@/assets/config/imm_setting_screen.yaml'

const home = ref(settingData.settings)
const tableData = ref([])
const showModal = ref(false)
const selectedRows = ref([])

const newRow = ref({
  設備グループID: '',
  設備機番: '',
  設備グループ名称: '',
  在庫管理グループID: '',
  在庫管理グループ名称: '',
  基準在庫日数: '',
  基準在庫管理幅: '',
})

const fetchData = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/imm-setting')
    tableData.value = res.data
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const openModal = () => {
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
}

const addRow = () => {
  // Simulate posting to backend or directly push into table for now
  tableData.value.push({ ...newRow.value })
  closeModal()
}

onMounted(fetchData)


const toggleAll = (event) => {
  if (event.target.checked) {
    selectedRows.value = tableData.value.map(row => row.id) // or another unique field
  } else {
    selectedRows.value = []
  }
}

</script>