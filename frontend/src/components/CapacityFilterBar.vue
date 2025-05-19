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
            <!-- <select v-model="partNumber" @change="$emit('update-partNumber', partNumber)"
                :style="{ backgroundColor: pickedColor }"
                class="w-full px-3 py-1.5 rounded text-white text-sm outline-none ">
                <option disabled value="">{{ home.filter.part_number }}</option>
                <option v-for="(m, i) in partNumbers" :key="i" :value="m">{{ m }}</option>
            </select> -->
            <input v-model="partNumber" list="productNumberList" maxlength="4"
                @input="$emit('update-partNumber', partNumber)" :style="{ backgroundColor: pickedColor }"
                class="w-full px-3 py-1.5 rounded text-white text-sm outline-none" type="text"
                :placeholder="home.filter.part_number" />

            <datalist id="productNumberList">
                <option v-for="(num, index) in partNumbers" :key="'part-' + index" :value="String(num).slice(-4)" />
            </datalist>

            <select v-model="shipmentCategory" @change="$emit('update-shipment', shipmentCategory)"
                :style="{ backgroundColor: pickedColor }"
                class=" w-full px-3 py-1.5 rounded text-white text-sm outline-none ">
                <option disabled value="">{{ home.filter.shipment_category }}</option>
                <option v-for="(m, i) in shipments" :key="i" :value="m">{{ m }}</option>
            </select>

            <select v-model="manufacture" @change="$emit('update-manufacturer', manufacture)"
                :style="{ backgroundColor: pickedColor }"
                class="w-full px-3 py-1.5 rounded text-white text-sm outline-none ">
                <option disabled value="">{{ home.filter.manufacture }}</option>
                <option v-for="(m, i) in manufacturers" :key="i" :value="m">{{ m }}</option>
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
import homeData from "@/assets/config/availability.yaml"
import reset from '@/assets/images/reset.png'

const home = ref(homeData.availability)

const defineProps = defineProps({
    partNumbers: Array,
    shipments: Array,
    manufacturers: Array
})

const emit = defineEmits(['update-partNumber', 'update-shipment', 'update-manufacturer', 'search', 'export'])

const partNumber = ref('')
const shipmentCategory = ref('')
const manufacture = ref('')

const resetFilters = () => {
    partNumber.value = ''
    shipmentCategory.value = ''
    manufacture.value = ''

    emit('update-partNumber', '')
    emit('update-shipment', '')
    emit('update-manufacturer', '')
}


// const searchQuery = ref('')
const pickedColor = ref('#212121')




</script>