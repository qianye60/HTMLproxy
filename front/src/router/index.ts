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
  
  // 如果目标页面不需要认证，直接通过
  if (!to.meta.requiresAuth) {
    return true
  }
  
  // 如果已经登录且token存在，直接通过
  if (userStore.isLoggedIn && userStore.token) {
    return true
  }
  
  // 检查登录状态
  const authResult = await userStore.checkLoginStatus()
  
  // 路由访问控制 - 处理需要登录的页面
  if (!authResult.islogin) {
    // 未登录时保存目标路由并跳转到登录页
    if (to.path !== '/') {
      sessionStorage.setItem("lastRoute", to.fullPath)
    }
    return { name: 'login' }
  } 
  
  // 已登录用户访问登录页的处理
  if (to.name === 'login' && authResult.islogin) {
    // 已登录用户访问登录页，检查是否有保存的路由
    const savedRoute = sessionStorage.getItem("lastRoute")
    if (savedRoute) {
      sessionStorage.removeItem("lastRoute")
      return savedRoute
    }
    return { name: 'control' }
  }
  
  // 保存非登录页面的路由，用于刷新恢复
  if (to.path !== '/login') {
    sessionStorage.setItem("lastRoute", to.fullPath)
  }
  
  return true
})

export default router
