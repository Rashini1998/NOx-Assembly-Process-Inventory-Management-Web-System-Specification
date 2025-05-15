<template>
    <tr class="text-center border-t border-gray-100 text-sm bg-neutral-300">
      <!-- Product Number -->
      <td rowspan="2" class="align-middle border border-gray-100">{{ row.ProductNumber }}</td>
  
      <!-- Manufacturer with icon -->
      <td rowspan="2" class="py-2 px-3 text-left align-middle border border-gray-100">
        <div class="flex items-center space-x-1">
          <img :src="status" alt="status" class="h-4 w-4" />
          <span>{{ row.Manufacturer }}</span>
        </div>
      </td>
  
      <!-- Shipping Classification -->
      <td rowspan="2" class="align-middle border border-gray-100">{{ row.ShippingClassification }}</td>
  
      <!-- In-Process Inventory -->
      <td rowspan="2" class="align-middle border border-gray-100">{{ row.inProcessInventory }}</td>
  
      <!-- Stock Receipt Record -->
      <td rowspan="2" class="align-middle border border-gray-100">{{ row.StockReceiptRecord }}</td>
  
      <!-- Pre-Shipment Inventory -->
      <td rowspan="2" class="align-middle border border-gray-100">{{ row.PreShipmentInventory }}</td>
  
      <!-- Plan Values (top row) -->
      <td
        v-for="(item, index) in planRows"
        :key="'plan-' + index"
        :style="{ backgroundColor: index === 0 ? 'rgba(255,232,117,1)' : bg-neutral-300 }"
        class="border border-gray-100 h-9"
      >
        {{ item.plan }}
      </td>
  
      <!-- Available days -->
      <td rowspan="2" class="align-middle border border-gray-100">{{ row.available_days }}</td>
    </tr>
  
    <tr class="text-center border-b border-gray-100 text-sm bg-neutral-300">
      <!-- Remaining Inventory (bottom row) -->
      <td
        v-for="(item, index) in planRows"
        :key="'remaining-' + index"
        :style="{ backgroundColor: index === 0 ? 'rgba(255,232,117,1)' : bg-neutral-300}"
        class="border border-gray-100 h-9"
      >
        {{ item.remaining }}
      </td>
    </tr>
  </template>
  
  <script setup>
  import status from '@/assets/images/status-icon.png'
  import { computed } from 'vue';
  
  const props = defineProps({
    row: Object
  });
  
  const planRows = computed(() => {
    const plans = [
      props.row.Plan1 || 0,
      props.row.Plan2 || 0,
      props.row.Plan3 || 0,
      props.row.Plan4 || 0,
      props.row.Plan5 || 0,
      props.row.Plan6 || 0,
      props.row.Plan7 || 0,
    ];
  
    const initialInventory = props.row.PreShipmentInventory || 0;
    let cumulative = 0;
  
    return plans.map((plan) => {
      cumulative += plan;
      const remaining = initialInventory - cumulative;
      return {
        plan,
        remaining: remaining < 0 ? 0 : remaining,
      };
    });
  });
  </script>
  