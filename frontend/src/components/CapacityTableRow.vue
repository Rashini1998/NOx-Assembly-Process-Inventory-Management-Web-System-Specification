<template>
    <tr class="text-center border-t border-gray-200 text-sm" style="background-color:rgb(212 212 212);">
        <td>{{ row.ProductNumber }}</td>
        <td class="py-2 px-3 text-left">
            <div class="flex items-center space-x-1">
                <img :src="status" alt="status" class="h-4 w-4" />
                <span>{{ row.Manufacturer }}</span>
            </div>
        </td>
        <td>{{ row.ShippingClassification }}</td>
        <td>{{ row.a }}</td>
        <td>{{ row.StockReceiptRecord }}</td>
        <td>{{ row.PreShipmentInventory }}</td>
        <td>{{ row.Plan1 }}</td>
        <td>{{ row.b }}</td>

        <!-- {
    "Accessories": 0,
    "AirtightnessInspection": 0,
    "CharacteristicInspection": 90,
    "CharacteristicInspectionOddLot": 2,
    "FA": 2,
    "FAFractionalItems": 0,
    "Manufacturer": "GUSTO",
    "Plan1": 0,
    "Plan2": 0,
    "Plan3": 0,
    "Plan4": 0,
    "Plan5": 0,
    "Plan6": 0,
    "PreShipmentInventory": 100,
    "ProductNumber": "1144780012",
    "SCU": 0,
    "ShippingClassification": "国内・市販",
    "StockReceiptRecord": 50,
    "Updated": "Wed, 18 Sep 2024 14:34:00 GMT",
    "VisualInspection": 6
  }, -->

    </tr>
</template>

<script setup>
import status from '@/assets/images/status-icon.png'
// import { computed } from 'vue';

defineProps({
    row: Object
})

// const workStatusBgColor = computed(() => {
//     const status = String(props.row.WorkStatus);
//     if (status === '1') return 'white';
//     if (status === '2') return 'black';
//     if (status === '3') return 'red';
//     return 'transparent'

// })

// const workStatusTextColor = computed(() => {
//     const status = String(props.row.WorkStatus)
//     if (status === '2') return 'white' // when background is black
//     return 'black'
// })

</script>