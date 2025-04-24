<template>
    <header class="bg-black">
      <div class=" min-h-screen " v-if="help">
        <div class="bg-black shadow-md py-4 px-6">
          <h1 class="text-white text-3xl font-bold">
            {{ help.title }}
          </h1>
        </div>
  
        <div class="p-6 text-left space-y-4 text-white">
          <h2 class="text-xl font-semibold">{{ help.contact_section.title }}</h2>
          <p>{{ help.contact_section.office }}</p>
          <p>{{ help.contact_section.name }}</p>
          <p>{{ help.contact_section.email }}</p>
          <p>{{ help.contact_section.phone }}</p>
  
          <h2 class="text-xl font-semibold pt-6">{{ help.document_section.title }}</h2>
          <p>{{ help.document_section.document_path }}</p>
        </div>
      </div>
    </header>
  </template>
<script setup>
import { ref } from 'vue'
import helpData from '@/assets/config/help.yaml'

const help = ref(helpData.help)
</script>


  