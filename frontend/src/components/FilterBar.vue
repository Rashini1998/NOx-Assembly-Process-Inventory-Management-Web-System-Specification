<template>
  <div class="flex flex-wrap items-center gap-4 mb-4 bg-black px-4 py-2">
    <!-- <div class="flex items-center bg-gray-100 p-2 rounded">
      <MagnifyingGlassIcon class="h-5 w-5 text-gray-500 mr-2" />
      <input type="text" placeholder="絞込み検索" v-model="searchQuery" @input="$emit('search', searchQuery)"
        class="bg-transparent focus:outline-none" />
    </div> -->
    <div class="flex items-center  p-2 rounded shrink-0">
      <MagnifyingGlassIcon class="h-5 w-5 text-white text-xl mr-2 font-semibold" />
      <span class="text-white text-lg font-semibold">
        絞込み検索
      </span>
    </div>
<div class="flex flex-wrap flex-grow gap-x-4 gap-y-2">
<select 
    :style="{ backgroundColor: pickedColor }" 
    class="mr-2 mb-2 px-2 py-1 rounded text-white min-w-[120px]" 
  >
      <option>メーカー</option>
    </select>

    <select 
    :style="{ backgroundColor: pickedColor }" 
    class="mr-2 mb-2 px-2 py-1 rounded text-white min-w-[120px]" >
      <option>品番</option>
    </select>

    <select 
    :style="{ backgroundColor: pickedColor }" 
    class="mr-2 mb-2 px-2 py-1 rounded text-white min-w-[120px]" >
      <option>出荷区分</option>
    </select>
</div>
    


    <div class="ml-auto flex items-center gap-2 shrink-0 ">
      <span class="text-white">
        csv出力
      </span>

      <button
      :style="{ backgroundColor: pickedColor }" 
       @click="$emit('export')" class=" px-2 py-1 rounded text-white ">
        🡫
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { MagnifyingGlassIcon } from '@heroicons/vue/24/solid'

// const searchQuery = ref('')
const pickedColor = ref('#212121')
</script>
