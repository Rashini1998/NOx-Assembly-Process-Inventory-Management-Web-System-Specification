<template>
    <table class="w-full border-collapse table-auto text-sm border-gray-300 bg-black">
        <thead>

            <!-- Column Headers -->
            <tr class="bg-gray-700 text-black text-center h-12" style="background-color: rgba(128,128,128,255);">
                <th class="px-2 py-1 border ">{{ home.table.shelfTagID }}</th>
                <th class="px-2 py-1 border">{{ home.table.partNumber }}</th>
                <th class="px-2 py-1 border">{{ home.table.nextProcessName }}</th>
                <th class="px-2 py-1 border">{{ home.table.processingLot }}</th>
                <th class="px-1 py-1 border">{{ home.table.quantity }}</th>
                <th class="px-2 py-1 border">{{ home.table.workStatus }}</th>
                <th class="px-2 py-1 border">{{ home.table.tagRegistrationDate }}</th>
                <th class="px-2 py-1 border">{{ home.table.tagUpdateDate }}</th>
                <th class="px-0 py-1 border">{{ home.table.daysInStock }}</th>
            </tr>
        </thead>
        <tbody>
            <StatusTableRow v-for="(item, index) in data" :key="index" :row="item" />
        </tbody>
    </table>
</template>

<script setup>
import homeData from '@/assets/config/status.yaml'
import StatusTableRow from './StatusTableRow.vue'
import { ref } from 'vue'

const home = ref(homeData.status)

defineProps({
    data: Array
})

</script>