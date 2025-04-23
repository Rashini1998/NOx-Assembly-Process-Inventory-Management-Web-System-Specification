<template>
    <div class="flex items-center text-white space-x-4 ">
      <div class="font-semibold text-xl pl-2">{{ pageTitle }}</div>
      <div class="text-lg p-4">Last Updated Date</div>
      <img :src="refresh" alt="Refresh" class="h-4" />
    </div>
  </template>  
  
  <script setup>
  import { computed } from 'vue'
  import { useRoute } from 'vue-router'
  import refresh from '@/assets/refresh.png'
  
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
  </script>
  