<template>
    <table class="w-full border-collapse table-auto text-sm border-gray-300 bg-black">
        <thead>

            <!-- Column Headers -->
            <tr class="bg-gray-700 text-black text-center" style="background-color: rgba(128,128,128,255);">
                <th class="px-2 py-1 border " rowspan="2">{{ home.table.headers.part_number }}</th>
                <th class="px-2 py-1 border" rowspan="2">{{ home.table.headers.manufacture }}</th>
                <th class="px-2 py-1 border" rowspan="2">{{ home.table.headers.shipment_category }}</th>
                <th class="px-2 py-1 border" rowspan="2">{{ home.table.headers.in_process_inventory }}</th>
                <th class="px-1 py-1 border" rowspan="2">{{ home.table.headers.received_inventory }}</th>
                <th class="px-2 py-1 border" rowspan="2">{{ home.table.headers.pre_shipment_inventory }}</th>
                <!-- Grouped Inventory Headers -->
                <th class="px-2 py-1 border" colspan="7">{{ home.table.headers.inventory_quality }}</th>

                <th class="px-2 py-1 border" rowspan="2">{{ home.table.headers.available_days }}</th>
            </tr>
            <!-- Second Header Row -->
            <tr class="bg-gray-700 text-black text-center" style="background-color: rgba(128,128,128,255);">
                <th class="px-2 py-1 border">11/8(金)</th>
                <th class="px-2 py-1 border">11/9(土)</th>
                <th class="px-2 py-1 border">11/10(日)</th>
                <th class="px-2 py-1 border">11/11(月)</th>
                <th class="px-2 py-1 border">11/12(火)</th>
                <th class="px-2 py-1 border">11/13(水)</th>
                <th class="px-2 py-1 border">11/14(木)</th>
            </tr>
        </thead>
        <tbody>
            <CapacityTableRow v-for="(item, index) in data" :key="index" :row="item" />
        </tbody>
    </table>
</template>

<script setup>
import homeData from '@/assets/config/availability.yaml'
import CapacityTableRow from './CapacityTableRow.vue'
import { ref } from 'vue'

const home = ref(homeData.availability)

defineProps({
    data: Array
})

</script>