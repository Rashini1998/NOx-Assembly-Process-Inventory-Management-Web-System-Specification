<template>
    <div class="flex items-center text-white space-x-4 ">
      <div class="font-semibold text-xl pl-2">{{ pageTitle }}</div>
      <div class="text-sm p-2">{{ home.title.updatedate }}</div>
      <div class="text-sm p-2">{{ home.title.updateFrequency }}</div>
      <button 
        @click="$emit('')" 
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
  const pickedColor = ref('#212121')
  const home = ref(homeData.home)
  </script>
  