<template>
  <div class="flex items-center gap-4 mb-4 bg-black px-4 py-2">

    <!-- Left: Search Label + Icon -->
    <div class="flex items-center shrink-0">
      <MagnifyingGlassIcon class="h-5 w-5 text-white mr-2" />
      <span class="text-white text-sm font-medium">
        {{ home.filter.search }}

      </span>
    </div>

    <!-- Middle: Selects take all remaining space -->
    <div class="flex flex-grow gap-3">
      <input v-model="tagId" list="tagIdList" @input="$emit('update-tagId', tagId)"
        :style="{ backgroundColor: pickedColor }" class="w-full px-3 py-1.5 rounded text-white text-sm outline-none"
        type="text" :placeholder="home.filter.shelfTagID" />
      <datalist id="tagIdList">
        <option v-for="(id, index) in tagIds" :key="'tag-' + index" :value="id" />
      </datalist>
      <input v-model="partNumber" list="partNumberList" maxlength="4" @input="$emit('update-partNumber', partNumber)"
        :style="{ backgroundColor: pickedColor }" class="w-full px-3 py-1.5 rounded text-white text-sm outline-none"
        type="text" :placeholder="home.filter.partNumber" />

      <datalist id="partNumberList">
        <option v-for="(num, index) in partNumbers" :key="'part-' + index" :value="String(num).slice(-4)" />
      </datalist>
      <select v-model="nextProcessName" @change="$emit('update-nextProcessName', nextProcessName)"
        :style="{ backgroundColor: pickedColor }" class=" w-full px-3 py-1.5 rounded text-white text-sm outline-none ">
        <option disabled value="">{{ home.filter.nextProcessName }}</option>
        <option v-for="(m, i) in nextProcessNames" :key="i" :value="m">{{ m }}</option>
      </select>

      <select v-model="workStatus" @change="$emit('update-workStatus', workStatus)"
        :style="{ backgroundColor: pickedColor }" class="w-full px-3 py-1.5 rounded text-white text-sm outline-none ">
        <option disabled value="">{{ home.filter.workStatus }}</option>
        <option v-for="(m, i) in workStatuses" :key="i" :value="m">{{ m }}</option>
      </select>
    </div>

    <!-- Right: CSV Export -->
    <div class="ml-auto flex items-center gap-2 shrink-0">

      <!-- reset the filterd data -->
      <span class="text-white text-sm">{{ home.filter.reset }}</span>
      <button @click="resetFilters" class="px-2 py-1 rounded text-white text-sm"
        :style="{ backgroundColor: pickedColor }">
        <img :src="reset" alt="Reset" />
      </button>

      <!-- download csv -->
      <span class="text-white text-sm">{{ home.filter.csv }}</span>
      <button @click="$emit('export')" class="px-2 py-1 rounded text-cyan-400 text-xl w-10 "
        :style="{ backgroundColor: pickedColor }">
        ⤓
      </button>
    </div>

  </div>
</template>


<script setup>
import { ref } from 'vue'
import { MagnifyingGlassIcon } from '@heroicons/vue/24/solid'
import homeData from "@/assets/config/status.yaml"
import reset from '@/assets/images/reset.png'

const home = ref(homeData.status)

const defineProps = defineProps({
  tagIds: Array,
  nextProcessNames: Array,
  workStatuses: Array,
  partNumbers: Array,
})

// defineEmits(['updateManufacturer', 'updateProductNumber', 'updateClassification', 'search', 'export'])
const emit = defineEmits(['update-tagId', 'update-nextProcessName', 'update-workStatus', 'update-partNumber', 'search', 'export'])

const tagId = ref('')
const nextProcessName = ref('')
const workStatus = ref('')
const partNumber = ref('')


// const searchQuery = ref('')
const pickedColor = ref('#212121')

const resetFilters = () => {
  tagId.value = ''
  nextProcessName.value = ''
  workStatus.value = ''
  partNumber.value = ''

  emit('update-tagId', '')
  emit('update-nextProcessName', '')
  emit('update-workStatus', '')
  emit('update-partNumber', '')
}


</script>