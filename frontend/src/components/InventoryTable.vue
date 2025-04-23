<template>
  <table class="w-full border-collapse table-auto text-sm border-gray-300">
    <thead>
      <!-- Total Row -->
      <tr class="text-black font-bold text-center " style="background-color:rgb(212 212 216);">
        <th class="px-2 py-1 border" style="background-color: rgb(251 191 36);" colspan="4">工程合計</th>
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
      <tr class="bg-gray-700 text-black text-center" style="background-color: rgb(163 163 163);">
        <th class="px-2 py-1 border ">メーカー</th>
        <th class="px-2 py-1 border">ASSY品番</th>
        <th class="px-2 py-1 border">SUBASSY品番</th>
        <th class="px-2 py-1 border">出荷区分</th>
        <th class="px-2 py-1 border">気密検査</th>
        <th class="px-2 py-1 border">SCU</th>
        <th class="px-2 py-1 border">水蒸気検査</th>
        <th class="px-2 py-1 border">特性検査</th>
        <th class="px-2 py-1 border">特性検査 識数品</th>
        <th class="px-2 py-1 border">アクセサリ</th>
        <th class="px-2 py-1 border">FA</th>
        <th class="px-2 py-1 border">FA識数品</th>
        <th >外観検査</th>
        <th  style="background-color:rgb(251 191 36);">品番合計</th>
      </tr>
    </thead>
    <tbody>
        <TableRow v-for="(item, index) in data" :key="index" :row="item" />
      </tbody>
  </table>
</template>
<script setup>
import { computed } from 'vue'
import TableRow from './TableRow.vue'

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
</script>
