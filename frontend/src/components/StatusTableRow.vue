<template>
    <tr class="text-center border-t border-gray-200 text-sm" style="background-color:rgb(212 212 212);">
        <td class="py-2 px-3 text-left">
            <div class="flex items-center space-x-1">
                <img :src="status" alt="status" class="h-4 w-4" />
                <span>{{ row.ShelfTagID }}</span>
            </div>
        </td>
        <td>{{ row.PartNumber }}</td>
        <td>{{ row.NextProcessName }}</td>
        <td>{{ row.ProcessingLot }}</td>
        <td>{{ row.Quantity }}</td>

        <!-- WorkStatus cell with dynamic background color -->
        <td
            :style="{backgroundColor: workStatusBgColor,
                color: workStatusTextColor
            }"
        >{{ row.WorkStatus }}</td>
        <td>{{ row.ShelfTagRegistrationDate }}</td>
        <td>{{ row.ShelfTagUpdateDate }}</td>
        <td class="bg-red-600">{{ row.DurationOfStay }}</td>
    </tr>
  </template>
  
  <script setup>
  import status from '@/assets/images/status-icon.png'
import { computed } from 'vue';

const props  = defineProps({
    row: Object
  })

  const workStatusBgColor = computed(()=>{
    const status = String(props.row.WorkStatus);
    if (status === '1') return 'white';
    if (status === '2') return 'black';
    if (status === '3') return 'red';
    return 'transparent'

  })

  const workStatusTextColor = computed(() => {
  const status = String(props.row.WorkStatus)
  if (status === '2') return 'white' // when background is black
  return 'black'
})

  </script>
  