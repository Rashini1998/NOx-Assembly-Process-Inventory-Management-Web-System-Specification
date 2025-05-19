<template>
    <div class="flex items-center gap-4 mb-4 bg-black px-4 py-2">

        <!-- Left: Search Label + Icon -->
        <div class="flex items-center shrink-0">
            <Cog6ToothIcon class="h-5 w-5 text-white mr-2" />
            <span class="text-white text-sm font-medium">
                {{ home.settings.section_settings }}
            </span>
        </div>

        <!-- Middle: Selects take all remaining space -->
        <div class="flex flex-grow gap-3">

            <select v-model="startProcess" @change="onProcessChange" :style="{ backgroundColor: pickedColor }"
                class="w-full px-3 py-1.5 rounded text-white text-sm outline-none ">
                <option class="text-white" disabled value="">{{ home.settings.air_tightness_inspection }}</option>
                <!-- <option v-for="p in processes" :key="p" :value="p">{{ p }}</option> -->
                <option v-for="key in processKeys" :key="key" :value="key">
                    {{ processLabel[key] }}
                </option>
                <!-- <option v-for="key in processKeys" :key="key" :value="key">{{ processLabel[key] }}</option> -->
            </select>
            <select v-model="endProcess" @change="onProcessChange" :style="{ backgroundColor: pickedColor }"
                class=" w-full px-3 py-1.5 rounded text-white text-sm outline-none ">
                <option class="text-white" disabled value="">{{ home.settings.visual_inspection }}</option>
                <!-- <option v-for="p in processes" :key="p" :value="p">{{ p }}</option> -->
                <option v-for="key in processKeys" :key="key" :value="key">
                    {{ processLabel[key] }}
                </option>
                <!-- <option v-for="key in processKeys" :key="key" :value="key">{{ processLabel[key] }}</option> -->
            </select>
        </div>

        <div class="ml-auto flex items-center gap-2 shrink-0">

            <!-- reset the filterd data -->
            <!-- <span class="text-white text-sm">{{ home.filter.reset }}</span> -->
            <button @click="resetFilters" class="px-2 py-1 rounded text-white text-sm"
                :style="{ backgroundColor: pickedColor }">
                <img :src="reset" alt="Reset" />
            </button>
        </div>

    </div>
</template>
<script setup>
import { ref } from 'vue'
import { Cog6ToothIcon } from '@heroicons/vue/24/solid'
import homeData from "@/assets/config/availability.yaml"
import reset from '@/assets/images/reset.png'

const home = ref(homeData.availability)
const pickedColor = ref('#212121')

const startProcess = ref('')
const endProcess = ref('')

const processKeys = ['airtight_inspection', 'scu', 'water_vapor_inspection', 'characteristics_inspection','characteristics_inspection_odd','accessories','fa','fa_fractional', 'visual_inspection'];

const processLabel= {
    airtight_inspection: '気密検査',
    scu: 'SCU',
    water_vapor_inspection: '水蒸気検査',
    characteristics_inspection: '特性検査',
    characteristics_inspection_odd: '特性検査端数品',
    accessories: 'アクセサリ',
    fa:'FA',
    fa_fractional:'FA端数品',
    visual_inspection: '外観検査'
  };
  
const emit = defineEmits(['update-process-range'])
const onProcessChange = () => {
  emit('update-process-range', { start: startProcess.value, end: endProcess.value })
}

const resetFilters = () => {
    startProcess.value = '';
    endProcess.value = '';
    emit('update-process-range', { start: '', end: '' });
}

</script>