<script setup>
import "leaflet/dist/leaflet.css"
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";
const zoom = 7
const center = [-0.347, 36.1605]
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-12 gap-2 h-full">
    <div class="md:col-span-10">
      <l-map :zoom="zoom" :center="center">
        <l-tile-layer url="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png" />
      </l-map>
    </div>
    <div class="md:col-span-2 p-2 md:py-3 md:px-4">
      <h2 class="text-2xl font-semibold text-gray-900">Shapefiles</h2>
      <!-- List of Shapefiles -->
      <div class="flex">
        <router-link :to="'add'" class="btn-1 ml-auto">Add</router-link>
      </div>
    </div>
  </div>
</template>
