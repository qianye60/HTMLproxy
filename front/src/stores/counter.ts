import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCounterStore = defineStore('counter', () => {
  const email = ref('')
  const password = ref('')
  const username = ref('')
  const islogin = ref(false)

  return { email, password, username, islogin }
})