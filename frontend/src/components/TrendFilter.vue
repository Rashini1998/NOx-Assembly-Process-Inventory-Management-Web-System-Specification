<template>
    <div class="flex items-center gap-4 mb-4 bg-black px-4 py-2">
        <div class="flex items-center shrink-0">
            <Cog6ToothIcon class="h-5 w-5 text-white mr-2" />
            <span class="text-white text-sm font-medium">{{ trend.filter.conditionSettings }}</span>
        </div>

        <div class="flex flex-grow gap-3">
            <select :style="{ backgroundColor: pickedColor }" v-model="selectedProcess"
                @change="emit('update-process', selectedProcess)"
                class="w-full px-3 py-1.5 rounded text-white text-sm outline-none">
                <option disabled value="">{{ trend.filter.process }}</option>
                <option v-for="proc in processes" :key="proc" :value="proc">{{ proc }}</option>
            </select>

            <input v-model="partNumber" 
                @input="$emit('update-partNumber', partNumber)" :style="{ backgroundColor: pickedColor }"
                class="w-full px-3 py-1.5 rounded text-white text-sm outline-none" type="text"
                :placeholder="trend.filter.productNumber" />


            <div class="relative w-full min-w-[12rem]">
                <Datepicker v-model="startDate" @update:modelValue="emit('update-startDate', $event)"
                    :placeholder="trend.filter.startDate" :style="{ backgroundColor: pickedColor }"
                    class="w-full pl-10 pr-3 py-1.5 rounded text-white text-sm outline-none" />
                <svg xmlns="http://www.w3.org/2000/svg"
                    class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white pointer-events-none"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 7V3M16 7V3M3 11h18M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
            </div>

            <div class="relative w-full min-w-[12rem]">
                <Datepicker v-model="endDate" @update:modelValue="emit('update-endDate', $event)"
                    :placeholder="trend.filter.endDate" :style="{ backgroundColor: pickedColor }"
                    class="w-full pl-10 pr-3 py-1.5 rounded text-white text-sm outline-none" />
                <svg xmlns="http://www.w3.org/2000/svg"
                    class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white pointer-events-none"
                    fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M8 7V3M16 7V3M3 11h18M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
            </div>
        </div>

        <div class="ml-auto flex items-center gap-2 shrink-0">
            <!-- <span class="text-white text-sm">{{ trend.filter.reset }}</span>
            <button @click="resetFilters" class="px-2 py-1 rounded text-white text-sm"
                :style="{ backgroundColor: pickedColor }">
                <img :src="reset" alt="Reset" />
            </button> -->

            <span class="text-white text-sm">{{ trend.filter.csv }}</span>
            <button @click="$emit('export')" class="px-2 py-1 rounded text-cyan-400 text-xl w-10"
                :style="{ backgroundColor: pickedColor }">
                ⤓
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { Cog6ToothIcon } from '@heroicons/vue/24/solid'
import trendData from '@/assets/config/trend.yaml'
// import reset from '@/assets/images/reset.png'
import Datepicker from 'vue3-datepicker'

const trend = ref(trendData.trend)
const startDate = ref(null)
const endDate = ref(null)

const defineProps = defineProps({
    partNumbers: Array,
    // processes: Array
})

const processes = [
                    "FA",
                    "SCU",
                    "アクセサリ",
                    "外観検査",
                    "気密検査",
                    "水蒸気検査",
                    "特性検査",
                 ]

const emit = defineEmits(['update-partNumber', 'update-startDate', 'update-endDate', 'update-process', 'search', 'export'])

const partNumber = ref('')
const selectedProcess = ref('')
const pickedColor = ref('#212121')

// const resetFilters = () => {
//     partNumber.value = ''
//     selectedProcess.value = ''
//     emit('update-process', '')
//     emit('update-partNumber', '')
//     emit('update-startDate', null)
//     emit('update-endDate', null)

// }
</script>