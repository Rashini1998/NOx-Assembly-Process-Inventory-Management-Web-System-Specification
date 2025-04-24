<template>
    <tr class="text-center border-t border-gray-200 text-sm" style="background-color:rgb(212 212 212);">
      <td class="py-2 px-3 text-left">
        <div class="flex items-center space-x-1">
          <img :src="status" alt="status" class="h-4 w-4"  />
          <span>{{ row.manufacturer }}</span>
        </div>
      </td>
      <td>{{ row.assyNumber }}</td>
      <td>{{ row.subassyNumber }}</td>
      <td>{{ row.classification }}</td>
      <td>{{ row.airtightness }}</td>
      <td>{{ row.scu }}</td>
      <td>{{ row.waterVapor }}</td>
      <td>{{ row.inspection }}</td>
      <td>{{ row.fractional }}</td>
      <td>{{ row.accessories }}</td>
      <td>{{ row.fa }}</td>
      <td>{{ row.faFractional }}</td>
      <td>{{ row.visual }}</td>
      <td>{{ total }}</td>
    </tr>
  </template>
  
  <script setup>
  import status from '@/assets/images/status-icon.png'
  import { computed } from 'vue';

  const props=defineProps({
    row:Object
  })
  const total = computed(() => {
  return [
    'airtightness', 'scu', 'waterVapor',
    'inspection', 'fractional', 'accessories', 'fa',
    'faFractional', 'visual'
  ].reduce((sum, key) => sum + Number(props.row[key] || 0), 0)
})
  </script>
  