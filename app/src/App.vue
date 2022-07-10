<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
    <RouterView />
</template>

<style>
.btn-1 {
  @apply focus:outline-none text-white bg-green-700 hover:bg-green-800 focus:ring-4 focus:ring-green-300 font-medium
  rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-green-600 dark:hover:bg-green-700 dark:focus:ring-green-800
}
.btn-2 {
  @apply text-gray-900 bg-white border border-gray-300 focus:outline-none hover:bg-gray-100 focus:ring-4
  focus:ring-gray-200 font-medium rounded-lg text-sm px-5 py-2.5 mr-2 mb-2 dark:bg-gray-800 dark:text-white
  dark:border-gray-600 dark:hover:bg-gray-700 dark:hover:border-gray-600 dark:focus:ring-gray-700
}
</style>