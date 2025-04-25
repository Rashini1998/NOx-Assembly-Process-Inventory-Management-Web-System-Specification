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
      <select v-model="manufacturer" @change="$emit('update-manufacturer', manufacturer)"
        :style="{ backgroundColor: pickedColor }" class="w-full px-3 py-1.5 rounded text-white text-sm outline-none ">
        <option disabled value="">{{ home.filter.manufacture }}</option>
        <option v-for="(m, i) in manufacturers" :key="i" :value="m">{{ m }}</option>
      </select>

      <select v-model="productNumber" @change="$emit('update-product-number', productNumber)"
        :style="{ backgroundColor: pickedColor }" class=" w-full px-3 py-1.5 rounded text-white text-sm outline-none ">
        <option disabled value="">{{ home.filter.productNumber }}</option>
        <option v-for="(m, i) in productNumbers" :key="i" :value="m">{{ m }}</option>
      </select>

      <select v-model="classification" @change="$emit('update-classification', classification)"
        :style="{ backgroundColor: pickedColor }" class="w-full px-3 py-1.5 rounded text-white text-sm outline-none ">
        <option disabled value="">{{ home.filter.ShippingClassification }}</option>
        <option v-for="(m, i) in classifications" :key="i" :value="m">{{ m }}</option>
      </select>
    </div>

    <!-- Right: CSV Export -->
    <div class="ml-auto flex items-center gap-2 shrink-0">

      <!-- reset the filterd data -->
      <span class="text-white text-sm">{{ home.filter.reset }}</span>
      <button  @click="resetFilters"  class="px-2 py-1 rounded text-white text-sm" :style="{ backgroundColor: pickedColor }">
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
import homeData from "@/assets/config/home.yaml"
import reset from '@/assets/images/reset.png'

const home = ref(homeData.home)

const defineProps = defineProps({
  manufacturers: Array,
  productNumbers: Array,
  classifications: Array
})

// defineEmits(['updateManufacturer', 'updateProductNumber', 'updateClassification', 'search', 'export'])
const emit = defineEmits(['update-manufacturer', 'update-product-number', 'update-classification', 'search', 'export'])

const manufacturer = ref('')
const productNumber = ref('')
const classification = ref('')

// const searchQuery = ref('')
const pickedColor = ref('#212121')

const resetFilters = () => {
  manufacturer.value = ''
  productNumber.value = ''
  classification.value = ''

  emit('update-manufacturer', '')
  emit('update-product-number', '')
  emit('update-classification', '')
}


</script>
