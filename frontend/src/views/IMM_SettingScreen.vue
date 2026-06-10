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
        <button :disabled="selectedRows.length !== 1"  @click="openPermissionModal('edit')"
          class="flex items-center space-x-2 bg-zinc-800 hover:bg-zinc-700 disabled:bg-zinc-500 text-white px-3 py-1 rounded">
          <ArrowPathIcon class="h-5 w-5 text-white" />
          <span>{{ home.filter.editRow }}</span>
        </button>
        <button :disabled="selectedRows.length === 0" @click="deleteRows"
          class="flex items-center space-x-2 bg-zinc-800 hover:bg-zinc-700 disabled:bg-zinc-500 text-white px-3 py-1 rounded">
          <XMarkIcon class="h-5 w-5 text-white" />
          <span>{{ home.filter.deleteRow }}</span>
        </button>
        <!-- ✅ Save Button for Editing -->
        <div v-if="isEditing" class="flex justify-end mt-1">
          <button @click="saveEdit" class="flex items-center space-x-2 px-3 py-1 bg-blue-600 hover:bg-blue-400 text-white rounded">
            保存 (Save)
          </button>
        </div>
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
            <tr v-for="row in tableData" :key="row.id" class="text-sm" style="background-color:rgb(212 212 212);">
              <td class="p-2 border text-center">
                <input type="checkbox" v-model="selectedRows" :value="row.id" />
              </td>

              <td class="p-2 border text-right">{{ row.id }}</td>
              <td class="p-2 border text-right">{{ row.設備グループID }}</td>
              <td class="p-2 border text-right">{{ row.設備機番 }}</td>
              <td class="p-2 border text-right">{{ row.設備グループ名称 }}</td>
              <!-- <td class="p-2 border text-right">{{ row.在庫管理グループID }}</td> -->
              <td class="p-2 border text-right">
                <input v-if="isEditing && selectedRows.includes(row.id)" v-model="editedRows.在庫管理グループID"
                  class="bg-white border p-1 w-full" />
                <span v-else>{{ row.在庫管理グループID }}</span>
              </td>
              <!-- <td class="p-2 border text-right">{{ row.在庫管理グループ名称 }}</td> -->
              <td class="p-2 border text-right">
                <input v-if="isEditing && selectedRows.includes(row.id)" v-model="editedRows.在庫管理グループ名称"
                  class="bg-white border p-1 w-full" />
                <span v-else>{{ row.在庫管理グループ名称 }}</span>
              </td>
              <!-- <td class="p-2 border text-right">{{ row.基準在庫日数 }}</td>
                -->
              <td class="p-2 border text-right">
                <input v-if="isEditing && selectedRows.includes(row.id)" type="number" v-model="editedRows.基準在庫日数"
                  class="bg-white border p-1 w-full" />
                <span v-else>{{ row.基準在庫日数 }}</span>
              </td>
              <!-- <td class="p-2 border text-right">{{ row.基準在庫管理幅 }}</td> -->
              <td class="p-2 border text-right">
                <input v-if="isEditing && selectedRows.includes(row.id)" v-model="editedRows.基準在庫管理幅"
                  class="bg-white border p-1 w-full" />
                <span v-else>{{ row.基準在庫管理幅 }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- ✅ Save Button for Editing
      <div v-if="isEditing" class="flex justify-end mt-3">
        <button @click="saveEdit" class="px-4 py-2 bg-blue-700 hover:bg-blue-500 text-white rounded">
          保存 (Save)
        </button>
      </div> -->
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
            <!-- <button @click="addRow"
              class="px-4 py-1 rounded bg-blue-900 hover:bg-blue-600 text-white transition-colors">追加</button> -->
            <button @click="openPermissionModal('add')" class="px-4 py-1 rounded bg-blue-900 hover:bg-blue-600 text-white">
              追加
            </button>
          </div>
        </div>
      </div>
      <div v-if="showPermissionModal"
        class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
        <div class="bg-zinc-900 text-white p-6 rounded-lg w-[450px] shadow-lg">

          <h2 class="text-lg font-bold mb-4">
            権限画面
          </h2>

          <p class="mb-4">
            継続確認でデータベースに移動してもよろしいですか？
          </p>

          <div class="mb-4">
            <label class="block mb-2">
              パスワード
            </label>

            <input v-model="password" type="password" class="w-full bg-zinc-800 border border-zinc-600 p-2 rounded" />
          </div>

          <div class="flex justify-end space-x-2">
            <button @click="cancelPermission" class="px-4 py-2 bg-zinc-700 rounded hover:bg-zinc-600">
              キャンセル
            </button>

            <button @click="confirmPermission" class="px-4 py-2 bg-blue-700 rounded hover:bg-blue-500">
              OK
            </button>
          </div>

        </div>
      </div>

    </div>
  </header>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { PlusIcon, ArrowPathIcon, XMarkIcon } from '@heroicons/vue/24/solid'

import axios from 'axios'
import settingData from '@/assets/config/imm_setting_screen.yaml'

const home = ref(settingData.settings)
const tableData = ref([])
const showModal = ref(false)
const selectedRows = ref([])

const isEditing = ref(false)
const editedRows = ref({})

const permissionAction = ref('')

const newRow = ref({
  設備グループID: '',
  設備機番: '',
  設備グループ名称: '',
  在庫管理グループID: '',
  在庫管理グループ名称: '',
  基準在庫日数: '',
  基準在庫管理幅: '',
})

const showPermissionModal = ref(false)
const password = ref('')

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

// const openPermissionModal = () => {
//   showPermissionModal.value = true
// }

const openPermissionModal = (action) => {
  permissionAction.value = action
  showPermissionModal.value = true
}

const cancelPermission = () => {
  showPermissionModal.value = false
  password.value = ''
}

// const confirmAddRow = async () => {
//   try {
//     if (password.value !== 'admin123') {
//       alert('パスワードが正しくありません')
//       return
//     }

//     await axios.post(
//       'http://localhost:5000/api/imm-setting',
//       newRow.value
//     )

//     await fetchData()

//     showPermissionModal.value = false
//     showModal.value = false

//     password.value = ''

//     newRow.value = {
//       設備グループID: '',
//       設備機番: '',
//       設備グループ名称: '',
//       在庫管理グループID: '',
//       在庫管理グループ名称: '',
//       基準在庫日数: '',
//       基準在庫管理幅: '',
//     }

//   } catch (error) {
//     console.error('Error adding row:', error)
//   }
// }

const confirmPermission = async () => {
  try {
    const response = await axios.post(
      'http://localhost:5000/api/verify-password',
      {
        password: password.value
      }
    )

    if (!response.data.success) {
      alert('パスワードが正しくありません')
      return
    }

    if (permissionAction.value === 'add') {
      await addRow()
    }

    if (permissionAction.value === 'edit') {
      startEdit()
    }

    showPermissionModal.value = false
    password.value = ''

  } catch (error) {
    alert('パスワードが正しくありません')
  }
}


const addRow = async () => {
  await axios.post(
    'http://localhost:5000/api/imm-setting',
    newRow.value
  )

  await fetchData()

  showModal.value = false

  newRow.value = {
    設備グループID: '',
    設備機番: '',
    設備グループ名称: '',
    在庫管理グループID: '',
    在庫管理グループ名称: '',
    基準在庫日数: '',
    基準在庫管理幅: '',
  }
}

// const addRow = async () => {
//   // // Simulate posting to backend or directly push into table for now
//   // tableData.value.push({ ...newRow.value })
//   // closeModal()
//   try {
//     await axios.post(
//       'http://localhost:5000/api/imm-setting',
//       newRow.value
//     )
//     // reload table from beckend
//     await fetchData()

//     // reset form
//     newRow.value = {
//       設備グループID: '',
//       設備機番: '',
//       設備グループ名称: '',
//       在庫管理グループID: '',
//       在庫管理グループ名称: '',
//       基準在庫日数: '',
//       基準在庫管理幅: '',
//     }
//     closeModal()
//   } catch (error) {
//     console.error('Error adding row:', error)
//   }

// }

onMounted(fetchData)


const toggleAll = (event) => {
  if (event.target.checked) {
    selectedRows.value = tableData.value.map(row => row.id) // or another unique field
  } else {
    selectedRows.value = []
  }
}

// const startEdit = () => {
//   if (selectedRows.value.length === 1) {
//     const rowId = selectedRows.value[0]
//     const target = tableData.value.find(r => r.id === rowId)
//     editedRows.value = { ...target }
//     isEditing.value = true
//   }
// }

const startEdit = () => {
  if (selectedRows.value.length === 1) {
    const rowId = selectedRows.value[0]
    const target = tableData.value.find(r => r.id === rowId)

    console.log("Editing row:", target)

    editedRows.value = { ...target }
    isEditing.value = true
  }
}

// const saveEdit = async () => {
//   try {
//     await axios.put(`http://localhost:5000/api/imm-setting/${editedRows.value.id}`, editedRows.value)

//     // Update table locally
//     const idx = tableData.value.findIndex(r => r.id === editedRows.value.id)
//     if (idx !== -1) {
//       tableData.value[idx] = { ...editedRows.value }
//     }

//     isEditing.value = false
//     editedRows.value = {}
//     selectedRows.value = []
//   } catch (error) {
//     console.error("Error updating data:", error)
//   }
// }

const saveEdit = async () => {
  try {
    await axios.put(
      `http://localhost:5000/api/imm-setting/${editedRows.value.id}`,
      editedRows.value
    )

    // Reload from DB
    await fetchData()

    isEditing.value = false
    editedRows.value = {}
    selectedRows.value = []

  } catch (error) {
    console.error("Error updating data:", error)
  }
}

const deleteRows = async () => {
  try {
    await axios.post('http://localhost:5000/api/imm-setting/delete', {
      ids: selectedRows.value
    })

    tableData.value = tableData.value.filter(
      row => !selectedRows.value.includes(row.id)
    )

    selectedRows.value = []
  } catch (error) {
    console.error("Error deleting rows:", error)
  }
}
</script>