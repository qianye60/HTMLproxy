import { createApp } from 'vue'
import { createPinia } from 'pinia'
import axios from 'axios'

import App from './App.vue'
import router from './router'
import { useUserStore } from './stores/user'

// 配置axios默认baseURL
axios.defaults.baseURL = '/api'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// 在应用挂载前检查登录状态
router.isReady().then(async () => {
  const userStore = useUserStore()
  
  // 检查本地是否有token，如果有则验证
  const storedToken = localStorage.getItem('JWTtoken')
  if (storedToken) {
    try {
      await userStore.checkLoginStatus()
    } catch (error) {
      console.log('初始化时token验证失败')
    }
  }
  
  app.mount('#app')
})
