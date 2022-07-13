<script setup>
import "leaflet/dist/leaflet.css"
import axios from 'axios'
import { ref, computed } from 'vue'
// import { marker } from "leaflet/dist/leaflet-src.esm"
import { divIcon, marker  } from "leaflet"
import { LMap, LTileLayer, LGeoJson, LFeatureGroup } from "@vue-leaflet/vue-leaflet";

const zoom = 12
const center = [-0.347, 36.1605];
const shapefiles = ref({});
const map = ref('map')
const hidden = ref([])
const store = (async () => await axios.get('http://127.0.0.1:5000/api/shapefiles'))()
store.then(({data}) =>  { shapefiles.value = {...data, shapefiles: data.shapefiles.map(d => ({...d, show: !hidden.value.includes(d.table)}))} })
const colours = computed(() => shapefiles.value.shapefiles.reduce((a, b) => ({ ...a, [b.table]: "#000000".replace(/0/g, () => (~~(Math.random() * 16)).toString(16))}), {}))
const svg = (colour) =>  `
<svg width="36px" height="36px" viewBox="-4 0 36 36" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <g id="Vivid.JS" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
        <g id="Vivid-Icons" transform="translate(-125.000000, -643.000000)">
            <g id="Icons" transform="translate(37.000000, 169.000000)">
                <g id="map-marker" transform="translate(78.000000, 468.000000)">
                    <g transform="translate(10.000000, 6.000000)">
                        <path d="M14,0 C21.732,0 28,5.641 28,12.6 C28,23.963 14,36 14,36 C14,36 0,24.064 0,12.6 C0,5.641 6.268,0 14,0 Z" id="Shape" fill="${colour}"></path>
                        <circle id="Oval" fill="#ffffff" fill-rule="nonzero" cx="14" cy="14" r="7"></circle>
                    </g>
                </g>
            </g>
        </g>
    </g>
</svg>
`
const style = (shp, type) => {
  switch (type) {
    case 'ST_Point':
        return {}
    default:
      return {
          fillColor: colours.value[shp], weight: 2, opacity: 1, color: colours.value[shp], fillOpacity: 0.7
      }
  }
}
const pointToLayer = (name) => (feature, latLng) => marker(latLng, { icon: divIcon({ html: svg(colours.value[name]), className: 'bg-transparent', iconAnchor: [18, 36] }) })
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-12 gap-2 h-full">
    <div class="md:col-span-10">
      <l-map :zoom="zoom" :center="center" ref="map">
        <l-tile-layer url="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png" />
        <l-feature-group v-for="(group, name) in shapefiles.data" :key="name">
          <l-geo-json :geojson="group" :options="{style: style(name, group.geometry_type), pointToLayer: pointToLayer(name)}" v-if="(shapefiles.shapefiles.find(({table}) => table === name) || {show: true}).show"/>
        </l-feature-group>
      </l-map>
    </div>
    <div class="md:col-span-2 p-2 md:py-3 md:px-4 flex flex-col">
      <div class="grow">
        <h2 class="text-2xl font-semibold text-gray-900">Shapefiles</h2>
        <!-- List of Shapefiles -->
        <ul class="mt-6 text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg dark:bg-gray-700 dark:border-gray-600 dark:text-white">
          <li v-for="(shp, idx) in shapefiles.shapefiles" :class="['w-full px-4 py-2 flex', {'rounded-t-lg' : idx === 0}, idx+1 === shapefiles.shapefiles.length ? 'rounded-b-lg' : 'border-b border-gray-200 dark:border-gray-600']">
            <!--<span class="flex-none w-18 border-r"></span>-->
            <span class="grow pl-2 truncate">{{ shp.table }}</span>
            <div class="flex-none">
              <label :for="shp.table" class="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" v-model="shp.show" :id="shp.table" class="sr-only peer">
                <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
              </label>
            </div>
          </li>
        </ul>
      </div>
      <div class="flex-none flex">
        <router-link :to="'add'" class="btn-1 ml-auto">Add</router-link>
      </div>
    </div>
  </div>
</template>
