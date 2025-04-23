<template>
  <header 
  :style="{ backgroundColor: pickedColor }"
  class="fixed top-0 left-0 w-full  text-white px-4 py-3 flex items-center justify-between z-50 shadow">
      <div  class="flex items-center space-x-4 w-1/3">
        <img :src="logo" alt="Logo" class="h-8 mr-8" />
        <h4 class="text-sm">NOx組付け工程在庫管理システム</h4>
      </div>
      <div  class="flex justify-center w-1/3">
        <select v-model="selected" @change="navigateToPage"
          class="bg-black text-white font-semibold border-none px-2 py-1 rounded">
          <option value="/">リアルタイム中間在庫画面</option>
          <option value="/status">リアルタイム棚札ステータス</option>
          <option value="/capacity">リアルタイム中間在庫余力日数</option>
          <option value="/trend">中間在庫推移</option>
          <option value="/table">汎用テーブル表示</option>

        </select>
      </div>
      <div class="flex items-center justify-end space-x-2 w-1/3">
        <span class="text-sm">{{ now }}</span>
        <button class="px-2 py-1 rounded text-blue">
          <img :src="setting" alt="Logo" class="h-0.5 " />
        </button>
        <button class="px-2 py-1 rounded text-blue">
          <img :src="help" alt="Logo" class="h-0.5 mr-8" />
        </button>
      </div>

  </header>
</template>

<script setup>
import { ref, onMounted,watch } from 'vue'
import { useRouter,useRoute } from 'vue-router'
import logo from '@/assets/logo.png'
import setting from '@/assets/settings.png'
import help from '@/assets/help.png'


const router = useRouter();
const route = useRoute();
const selected = ref(route.path)

function navigateToPage() {
  router.push(selected.value)
}

watch(route,(newRoute)=>{
  selected.value=newRoute.path
})

// const now = ref('')
// const updateTime = () => {
//   const date = new Date()
//   now.value = date.toLocaleString('ja-JP', { hour12: false })
// }

// onMounted(() => {
//   updateTime()
//   setInterval(updateTime, 1000)
// })
const now = ref('')
const updateTime = () => {
  const date = new Date()
  const yyyy = date.getFullYear()
  const mm = String(date.getMonth() + 1).padStart(2, '0')
  const dd = String(date.getDate()).padStart(2, '0')
  const hh = String(date.getHours()).padStart(2, '0')
  const min = String(date.getMinutes()).padStart(2, '0')
  const ss = String(date.getSeconds()).padStart(2, '0')

  now.value = `${yyyy}/${mm}/${dd} ${hh}:${min}:${ss}`  // consistent format
}

onMounted(() => {
  updateTime()
  setInterval(updateTime, 1000)
})

const pickedColor = ref('#212121')
</script>
