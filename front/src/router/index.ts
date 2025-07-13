import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../pages/home.vue'
import LoginView from '../pages/login.vue'
import ControlView from '../pages/control.vue'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/control',
      name: 'control',
      component: ControlView,
      meta: { requiresAuth: true }
    },
  ],
})

/**
 * 全局路由守卫
 * 拦截需要登录的页面，检查用户登录状态
 */
router.beforeEach(async (to, from) => {
  const userStore = useUserStore()
  // 1. 已登录用户访问登录页，直接跳转到控制面板
  if (to.name === 'login' && (userStore.isLoggedIn || userStore.token)) {
    // 检查登录状态（防止刷新丢失）
    const authResult = await userStore.checkLoginStatus()
    if (authResult.islogin) {
      const savedRoute = sessionStorage.getItem("lastRoute")
      if (savedRoute) {
        sessionStorage.removeItem("lastRoute")
        return savedRoute
      }
      return { name: 'control' }
    }
  }
  // 2. 如果目标页面不需要认证，直接通过
  if (!to.meta.requiresAuth) {
    return true
  }
  // 3. 如果已经登录且token存在，直接通过
  if (userStore.isLoggedIn && userStore.token) {
    return true
  }
  // 4. 检查登录状态
  const authResult = await userStore.checkLoginStatus()
  // 5. 路由访问控制 - 处理需要登录的页面
  if (!authResult.islogin) {
    if (to.path !== '/') {
      sessionStorage.setItem("lastRoute", to.fullPath)
    }
    return { name: 'login' }
  }
  // 6. 其它逻辑...
  if (to.path === '/' && authResult.islogin) {
    return { name: 'control' }
  }
  if(to.name === 'control' && authResult.islogin){
    return { name: 'control' }
  }
  if (to.path !== '/login') {
    sessionStorage.setItem("lastRoute", to.fullPath)
  }
  return true
})

export default router
