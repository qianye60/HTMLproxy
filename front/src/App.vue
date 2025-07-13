<template>
  <header class="nav-header">
    <div class="nav-logo">
        <img src="/favicon.ico" alt="logo" class="owl-logo">
      <span class="nav-title">灵枭HTML代理</span>
    </div>
    <nav class="nav-links">
      <RouterLink to="/">首页</RouterLink>
      <RouterLink to="/login">登录</RouterLink>
    </nav>
  </header>
  <main>
    <RouterView/>
  </main>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style scoped>
.nav-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 32px;
  height: 64px;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
  box-shadow: 0 2px 8px 0 rgba(0,0,0,0.03);
  position: sticky;
  top: 0;
  z-index: 1000;
}
.nav-logo {
  display: flex;
  align-items: center;
}
.owl-logo {
  width: 40px;
  height: 40px;
  margin-right: 12px;
}
.nav-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #22c55e;
  letter-spacing: 2px;
}
.nav-links {
  display: flex;
  gap: 32px;
}
.nav-links a {
  color: #374151;
  font-size: 1rem;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}
.nav-links a.router-link-active,
.nav-links a:hover {
  color: #22c55e;
}
@media (max-width: 600px) {
  .nav-header {
    flex-direction: column;
    height: auto;
    padding: 12px;
  }
  .nav-links {
    gap: 16px;
    margin-top: 8px;
  }
}
</style>