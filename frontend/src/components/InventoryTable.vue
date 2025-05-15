<template>
  <table class="w-full border-collapse table-auto text-sm border-gray-300 bg-black">
    <thead>
      <!-- Total Row -->
      <tr class="text-black font-bold text-center h-12" style="background-color:rgb(212 212 216);">
        <th class="px-2 py-1 border" style="background-color: rgb(251 191 36);" colspan="4">{{ home.table.headers.totalProducts }}</th>
        <th class="px-2 py-1 border">{{ total.airtightness }}</th>
        <th class="px-2 py-1 border">{{ total.scu }}</th>
        <th class="px-2 py-1 border">{{ total.waterVapor }}</th>
        <th class="px-2 py-1 border">{{ total.inspection }}</th>
        <th class="px-2 py-1 border">{{ total.fractional }}</th>
        <th class="px-2 py-1 border">{{ total.accessories }}</th>
        <th class="px-2 py-1 border">{{ total.fa }}</th>
        <th class="px-2 py-1 border">{{ total.faFractional }}</th>
        <th class="px-2 py-1 border">{{ total.visual }}</th>
        <th class="px-2 py-1 border" style="background-color:rgb(10 10 10);"></th>
      </tr>

      <!-- Column Headers -->
      <tr class="bg-gray-700 text-black text-center h-12" style="background-color: rgba(128,128,128,255);">
        <th class="px-2 py-1 border ">{{ home.table.headers.manufacture }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.ASSY_Part_Number }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.SUBASSY_Part_Number }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.Shipping_Classification }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.Airtightness_Inspection }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.SCU }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.Water_Vapor_Test }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.Characteristic_Inspection }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.Characteristic_Inspection_Fractional_Items }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.Accessories }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.FA }}</th>
        <th class="px-2 py-1 border">{{ home.table.headers.FA_Fractional_Items }}</th>
        <th >{{ home.table.headers.Visual_Inspection }}</th>
        <th  style="background-color:rgb(251 191 36);">{{ home.table.headers.total }}</th>
      </tr>
    </thead>
    <tbody>
        <TableRow v-for="(item, index) in data" :key="index" :row="item" />
      </tbody>
  </table>
</template>
<script setup>
import { computed, ref } from 'vue'
import TableRow from './TableRow.vue'
import homeData from '@/assets/config/home.yaml'


const props = defineProps({
  data: {
    type: Array,
    required: true
  }
})

const total = computed(() => {
  const initial = {
    airtightness: 0,
    scu: 0,
    waterVapor: 0,
    inspection: 0,
    fractional: 0,
    accessories: 0,
    fa: 0,
    faFractional: 0,
    visual: 0,

  }

  return props.data.reduce((acc, row) => {
    acc.airtightness += row.airtightness || 0
    acc.scu += row.scu || 0
    acc.waterVapor += row.waterVapor || 0
    acc.inspection += row.inspection || 0
    acc.fractional += row.fractional || 0
    acc.accessories += row.accessories || 0
    acc.fa += row.fa || 0
    acc.faFractional += row.faFractional || 0
    acc.visual += row.visual || 0

    return acc
  }, initial)
})
const home = ref(homeData.home)
</script>
