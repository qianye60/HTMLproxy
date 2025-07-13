import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },  
  server: {
    host: '127.0.0.1',
    port: 40001,
    hmr : true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:40000',
        changeOrigin: true,
        secure: false,
      },
      '/html': {
        target: 'http://127.0.0.1:40000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
})
