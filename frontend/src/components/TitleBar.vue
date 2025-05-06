<template>
    <div class="flex items-center text-white space-x-3 ">
      <div class="font-semibold text-xl">{{ pageTitle }}</div>
      <div class="text-sm">{{ home.title.updatedate }}</div>
      <div class="text-sm">{{ updatedTime }}</div>
      <div class="text-sm">{{ home.title.updateFrequency }}</div>
      <div class="text-sm">{{ home.title.oneMin }}</div>
      <button 
        @click="$emit('refresh')" 
        class="px-2 py-1 rounded text-white text-sm"
        :style="{ backgroundColor: pickedColor }">
        <img :src="refresh"  alt="Refresh"  />
      </button>
      
    </div>
  </template>  
  
  <script setup>
  import { computed, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import refresh from '@/assets/images/refresh.png'
  import homeData from '@/assets/config/home.yaml'
  
  const route = useRoute()
  const pickedColor = ref('#212121')
  const home = ref(homeData.home)
  const defineProps = defineProps({ updatedTime: String })
  
  const pageTitle = computed(() => {
    switch (route.path) {
      case '/':
        return 'リアルタイム中間在庫画面'
      case '/status':
        return 'リアルタイム棚札ステータス'
      case '/capacity':
        return 'リアルタイム中間在庫余力日数'
      case '/trend':
        return '中間在庫推移'
      case '/table':
        return '汎用テーブル表示'
      default:
        return 'Hello'
    }
  })


  </script>
  