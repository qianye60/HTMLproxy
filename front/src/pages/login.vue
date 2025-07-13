<template>
  <div class="login-container">
    <div class="form-box">
      <form class="form" @submit.prevent="register">
        <span class="title">登录/注册</span>
        <span class="subtitle">使用邮箱登录/注册</span>
        <div class="form-container">
          <input v-if="isregister" type="text" class="input" placeholder="用户名" v-model="formData.username">
          <input type="email" class="input" placeholder="邮箱" v-model="formData.email">
          <input type="password" class="input" placeholder="密码" v-model="formData.password">
        </div>
        <div v-if="errorMsg" style="color:red;margin-bottom:8px;">{{ errorMsg }}</div>
        <button v-if="!isregister">登录</button>
        <button v-if="isregister">注册</button>
      </form>
      <div class="form-section">
        <p>
          没有账号？
          <a href="" @click.prevent="toggleRegister">{{ isregister ? '登录' : '注册' }}</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '../stores/user'
import axios from "axios";
import { useRouter } from 'vue-router'

const router = useRouter()
const userStore = useUserStore()
const isregister = ref(false)
const errorMsg = ref('')

// 表单数据
const formData = ref({
  username: '',
  email: '',
  password: ''
})

function validateForm() {
  if (isregister.value && !formData.value.username) {
    errorMsg.value = '请输入用户名';
    return false;
  }
  if (!formData.value.email) {
    errorMsg.value = '请输入邮箱';
    return false;
  }
  if (!/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(formData.value.email)) {
    errorMsg.value = '邮箱格式不正确';
    return false;
  }
  if (!formData.value.password || formData.value.password.length < 6) {
    errorMsg.value = '密码至少6位';
    return false;
  }
  errorMsg.value = '';
  return true;
}

async function register(){
    if (!validateForm()) return;
    try {
      if(isregister.value == false){//登录
        const response = await axios.post("/login", {
          email: formData.value.email,
          password: formData.value.password
        })
        const { access_token } = response.data
        userStore.setToken(access_token)
        
        // 立即更新登录状态
        userStore.isLoggedIn.value = true
        
        // 等待一下确保状态更新
        await new Promise(resolve => setTimeout(resolve, 100))
        
        router.push('/control')
      }
      else{
        const response = await axios.post("/register",{
          username: formData.value.username,
          email: formData.value.email,
          password: formData.value.password
        })
        alert("注册成功!请登录")
        isregister.value = false
        formData.value.username = ''
      }
    } catch (err) {
      console.error('请求错误:', err);
      if (err.response && err.response.data && err.response.data.detail) {
        errorMsg.value = err.response.data.detail
      } else {
        errorMsg.value = '请求失败，请稍后重试';
      }
    }
}

function toggleRegister() {
  isregister.value = !isregister.value;
  errorMsg.value = '';
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f8fafc;
}
.form-box {
  max-width: 320px;
  background: #f1fdf4;
  overflow: hidden;
  border-radius: 16px;
  color: #010101;
  box-shadow: 0 4px 24px rgba(34,197,94,0.08);
}
.form {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 32px 24px 24px;
  gap: 16px;
  text-align: center;
}
.title {
  font-weight: bold;
  font-size: 1.6rem;
  color: #22c55e;
}
.subtitle {
  font-size: 1rem;
  color: #16a34a;
}
.form-container {
  overflow: hidden;
  border-radius: 8px;
  background-color: #fff;
  margin: 1rem 0 .5rem;
  width: 100%;
}
.input {
  background: none;
  border: 0;
  outline: 0;
  height: 40px;
  width: 100%;
  border-bottom: 1px solid #e0e0e0;
  font-size: .95rem;
  padding: 8px 15px;
}
.form-section {
  padding: 16px;
  font-size: .85rem;
  background-color: #e0f7ec;
  box-shadow: rgb(0 0 0 / 8%) 0 -1px;
}
.form-section a {
  font-weight: bold;
  color: #22c55e;
  transition: color .3s ease;
}
.form-section a:hover {
  color: #16a34a;
  text-decoration: underline;
}
.form button {
  background-color: #22c55e;
  color: #fff;
  border: 0;
  border-radius: 24px;
  padding: 10px 16px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color .3s ease;
  box-shadow: 0 2px 8px rgba(34,197,94,0.08);
}
.form button:hover {
  background-color: #16a34a;
}
</style>
