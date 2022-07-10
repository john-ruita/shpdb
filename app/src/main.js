import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import "./assets/base.css"
import 'flowbite';

window.app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
