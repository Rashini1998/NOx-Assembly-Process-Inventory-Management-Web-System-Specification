<template>
  <header :style="{ backgroundColor: pickedColor }"
    class="fixed top-0 left-0 w-full  text-white px-4 py-3 flex items-center justify-between z-50 shadow">
    <div class="flex items-center space-x-4 w-1/3">
      <img :src="logo" alt="Logo" class="h-12 mr-2" />
      <h4 class="text-sm font-semibold">{{ home.header.companyName }}</h4>
    </div>
    <div class="flex justify-center w-1/3">
      <select v-model="selected" @change="navigateToPage"
        class="bg-black text-white font-semibold border-none px-2 py-1 rounded">
        <option value="/">{{ home.header.page01 }}</option>
        <option value="/status">{{ home.header.page02 }}</option>
        <option value="/capacity">{{ home.header.page03 }}</option>
        <option value="/trend">{{ home.header.page04 }}</option>
        <option value="/table">{{ home.header.page05 }}</option>
        <option value="/help">{{ home.header.page06 }}</option>

      </select>
    </div>
    <div class="flex items-center justify-end space-x-2 w-1/3">
      <span class="text-sm">{{ now }}</span>
      <button class="px-2 py-1 rounded text-blue">
        <img :src="setting" alt="Setting" class="h-4 " />
      </button>
      <button class="px-2 py-1 rounded text-blue" @click="goToHelp">
        <img :src="help" alt="Help" class="h-4 mr-3" />
      </button>
    </div>

  </header>
</template>

<script setup>

import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import logo from '@/assets/images/logo.png'
import setting from '@/assets/images/settings.png'
import help from '@/assets/images/help.png'
import homeData from "@/assets/config/home.yaml"

const router = useRouter();
const route = useRoute();
const selected = ref(route.path)

function navigateToPage() {
  router.push(selected.value)
}

watch(route, (newRoute) => {
  selected.value = newRoute.path
})

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

const goToHelp = () => {
  router.push({ name: 'HelpScreen' });
};

const home = ref(homeData.home)
</script>
