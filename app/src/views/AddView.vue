<script setup>
import { XIcon } from '@heroicons/vue/solid'
import { ref } from 'vue'
import axios from 'axios'

const shapefile = ref({ shp: null, shx: null, dbf: null })
const others = ref([])
const errors = ref({ shp: '', shx: '', dbf: '' })
const submit = ref('Submit')
const extensions = {cpg: 'bg-pink-600', sbx: 'bg-purple-600', prj: 'bg-yellow-500', sbn: 'bg-green-500'}

const addFiles = (e) => others.value = [...(e.dataTransfer || e.target).files].filter(f => ['cpg', 'sbn', 'sbx', 'prj'].includes(extension(f.name)))
const filesize = (size) => {
  let i = Math.floor(Math.log(size) / Math.log(1024));
  return ( size / Math.pow(1024, i) ).toFixed(2) * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i];
};
const extension = (f) => f.slice((Math.max(0, f.lastIndexOf('.')) || Infinity) + 1)
const addFile = (e, ext) => {
  if (ext !== extension(e.target.files[0].name)) {
    errors.value[ext] = `Please select the correct file format (${ext})`
    document.getElementById(ext).value = null
  } else {
    errors.value[ext] = ''
    shapefile.value[ext] = e.target.files[0]
  }
}
const save = () => {
  submit.value = 'Processing'
  if (validate() && Object.values(errors.value).every(x => x === null || x === '')){
    submit.value = 'Uploading'
    const data = new FormData();
    [ ...Object.values(shapefile.value), ...others.value ].forEach(u => { data.append('shapefile[]', u) })
    data.append('name', shapefile.value.shp.name)
    axios.post('http://127.0.0.1:5000/api/upload', data)
        .then(res => {
          submit.value = 'Submit'
        })
        .catch(err => {
          console.log(err)
        })
  }
  submit.value = 'Submit'
}
const validate = () => {
  if (!shapefile.value.shp) {
    errors.value.shp = 'This file is required'
  }
  if (!shapefile.value.shx) {
    errors.value.shx = 'This file is required'
  }
  if (!shapefile.value.dbf) {
    errors.value.dbf = 'This file is required'
  }
  return !Object.values(shapefile.value).every(x => x === null || x === '')
}
</script>

<template>
  <div class="flex h-full">
    <div class="w-full h-full m-2 md:my-12 md:mx-48">
      <div class="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
        <h2 class="text-2xl font-semibold text-gray-900">Import Shapefile</h2>

        <div class="grid grid-cols-1 gap-2">
          <div>
            <label class="block text-sm font-medium text-gray-900 dark:text-gray-300" for="shp">Select .shp (feature geometry)</label>
            <input accept=".shp" class="file-input" @change="addFile($event, 'shp')" id="shp" type="file">
            <p class="text-sm text-red-600 dark:text-red-500" v-text="errors.shp" v-if="errors.shp"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900 dark:text-gray-300" for="shx">Select .shx (index of feature geometry)</label>
            <input accept=".shx" class="file-input" @change="addFile($event, 'shx')" id="shx" type="file">
            <p class="text-sm text-red-600 dark:text-red-500" v-text="errors.shx" v-if="errors.shx"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-900 dark:text-gray-300" for="dbf">Select .dbf (attribute information)</label>
            <input accept=".dbf" class="file-input" @change="addFile($event, 'dbf')" id="dbf" type="file">
            <p class="text-sm text-red-600 dark:text-red-500" v-text="errors.dbf" v-if="errors.dbf"/>
          </div>
          <div class="flex justify-center items-center w-full" @dragover.prevent @drop.prevent>
            <label for="dropzone-file" @drop="addFiles" @change="addFiles" class="flex flex-col justify-center items-center w-full p-2 bg-gray-50 rounded-lg border-2 border-gray-300 border-dashed cursor-pointer dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
              <div v-if="others.length" class="py-4">
                <ul role="list" class="grid grid-cols-1 gap-5 sm:gap-6 sm:grid-cols-2 lg:grid-cols-4">
                  <li v-for="(file, idx) in others" :key="file.name" class="col-span-1 flex shadow-sm rounded-md">
                    <div :class="[extensions[extension(file.name)], 'flex-shrink-0 flex items-center justify-center w-16 text-white text-sm font-medium rounded-l-md uppercase']">
                      {{ extension(file.name) }}
                    </div>
                    <div class="flex-1 flex items-center justify-between border-t border-r border-b border-gray-200 bg-white rounded-r-md truncate">
                      <div class="flex-1 px-4 py-2 text-sm truncate">
                        <p class="text-gray-900 font-medium hover:text-gray-600">{{ file.name }}</p>
                        <p class="text-gray-500">{{ filesize(file.size) }}</p>
                      </div>
                      <div class="flex-shrink-0 pr-2">
                        <button type="button" class="w-8 h-8 bg-white inline-flex items-center justify-center text-gray-400 rounded-full bg-transparent hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                          <span class="sr-only">Open options</span>
                          <XIcon class="w-5 h-5" aria-hidden="true" />
                        </button>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
              <div v-else class="flex flex-col justify-center items-center pt-5 pb-6 md:py-12">
                <svg class="mb-3 w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Click to add non-mandatory files</span>  or drag and drop</p>
                <p class="text-xs text-gray-500 dark:text-gray-400">CPG, PRJ, SBN or SBX</p>
              </div>
              <input accept=".cpg,.prj,.sbn,.sbx" id="dropzone-file" type="file" class="hidden" multiple>
            </label>
          </div>
        </div>

        <div class="flex justify-between mt-2">
          <router-link :to="'/'" class="btn-2" v-text="'Cancel'"/>
          <button class="btn-1 w-36" :disabled="submit!=='Submit'" @click="save">
            <span class="mr-auto">{{ submit }}</span>
            <span :class="{'loading': submit!=='Submit'}" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.file-input{
  @apply block w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer
  dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400
}

.loading:after {
  overflow: hidden;
  display: inline-block;
  vertical-align: bottom;
  -webkit-animation: ellipsis steps(4,end) 900ms infinite;
  animation: ellipsis steps(4,end) 900ms infinite;
  content: "\2026"; /* ascii code for the ellipsis character */
  width: 0;
}

@keyframes ellipsis {
  to {
    width: 1.25em;
  }
}

@-webkit-keyframes ellipsis {
  to {
    width: 1.25em;
  }
}
</style>