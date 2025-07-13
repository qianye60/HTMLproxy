import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'

// 配置axios默认baseURL
axios.defaults.baseURL = '/api'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
