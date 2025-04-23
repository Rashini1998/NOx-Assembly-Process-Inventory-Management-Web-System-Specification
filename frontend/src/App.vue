<!-- <template>
  <router-view />
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style> -->

<template>
  <div class="bg-gray-100 min-h-screen pt-20">
    <HeaderBar />
    <router-view /> <!-- Every page will render here -->
  </div>
</template>

<script setup>
import HeaderBar from '@/components/HeaderBar.vue'

</script>

<style>
body {
  margin: 0;
}
</style>
