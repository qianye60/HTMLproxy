<template>
  <div class="ai-generator">
    <div class="generator-header">
      <div class="header-content">
        <div class="title-section">
          <div class="title-icon">
            <Zap />
          </div>
          <div>
            <h1>AI网站生成器</h1>
            <p>通过AI快速生成您的专属HTML网站</p>
          </div>
        </div>
        
        <!-- 使用统计 -->
        <div class="usage-stats">
          <div class="usage-item">
            <span class="usage-label">今日已用</span>
            <span class="usage-value">{{ usageStats.used_today }}/{{ usageStats.total_limit }}</span>
          </div>
          <div class="usage-progress">
            <div 
              class="progress-bar"
              :style="{ width: `${(usageStats.used_today / usageStats.total_limit) * 100}%` }"
            ></div>
          </div>
          <div class="remaining-text">
            剩余 {{ usageStats.remaining_today }} 次
          </div>
        </div>
      </div>
    </div>

    <div class="generator-container">
      <!-- 左侧 - 生成区域 -->
      <div class="generate-section">
        <div class="generate-card">
          <div class="card-header">
            <h2>描述您的网站需求</h2>
            <p>详细描述您想要的网站类型、风格、功能等</p>
          </div>
          
          <form @submit.prevent="generateWebsite" class="generate-form">
            <div class="form-group">
              <textarea
                v-model="prompt"
                placeholder="例如：创建一个现代化的个人作品集网站，包含深色主题、响应式设计、作品展示区域和联系方式..."
                :disabled="isGenerating"
                required
                rows="6"
              ></textarea>
            </div>
            
            <div class="form-actions">
              <button 
                type="submit" 
                class="generate-btn"
                :disabled="isGenerating || usageStats.remaining_today <= 0"
              >
                <div v-if="isGenerating" class="loading-spinner">
                  <Loader2 />
                </div>
                <Sparkles v-else />
                {{ isGenerating ? '正在生成...' : '生成网站' }}
              </button>
              
              <div v-if="usageStats.remaining_today <= 0" class="limit-warning">
                今日生成次数已用完，请明天再试
              </div>
            </div>
          </form>
        </div>

        <!-- 生成历史 -->
        <div class="history-section">
          <div class="history-header">
            <h3>生成历史</h3>
            <button @click="fetchHistory" class="refresh-btn">
              <RefreshCw />
              刷新
            </button>
          </div>
          
          <div class="history-list">
            <div v-if="generationHistory.length === 0" class="empty-history">
              <Clock class="empty-icon" />
              <p>暂无生成记录</p>
            </div>
            
            <div 
              v-for="item in generationHistory" 
              :key="item.id" 
              class="history-item"
              @click="selectHistory(item)"
            >
              <div class="history-content">
                <p class="history-prompt">{{ item.prompt }}</p>
                <p class="history-time">{{ formatDate(item.generation_time) }}</p>
              </div>
              <ChevronRight class="history-arrow" />
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧 - 预览区域 -->
      <div class="preview-section">
        <div class="preview-card">
          <div class="preview-header">
            <h3>实时预览</h3>
            <div class="preview-actions">
              <button 
                v-if="generatedContent" 
                @click="saveAsFile" 
                class="save-btn"
              >
                <Save />
                保存文件
              </button>
              <button 
                v-if="generatedContent" 
                @click="viewFullScreen" 
                class="fullscreen-btn"
              >
                <Expand />
                全屏预览
              </button>
            </div>
          </div>
          
          <div class="preview-container">
            <div v-if="!generatedContent && !isGenerating" class="preview-placeholder">
              <Globe class="placeholder-icon" />
              <h4>预览区域</h4>
              <p>生成的网站将在此处显示</p>
            </div>
            
            <div v-if="isGenerating" class="loading-preview">
              <div class="loading-animation">
                <Loader2 class="loading-icon" />
              </div>
              <h4>AI正在生成您的网站...</h4>
              <p>请稍候，这可能需要几秒钟</p>
            </div>
            
            <iframe
              v-if="generatedContent && !isGenerating"
              :srcdoc="generatedContent"
              class="preview-iframe"
              title="网站预览"
            ></iframe>
          </div>
        </div>
      </div>
    </div>

    <!-- 全屏预览弹窗 -->
    <div v-if="showFullScreen" class="fullscreen-modal" @click="closeFullScreen">
      <div class="fullscreen-content" @click.stop>
        <div class="fullscreen-header">
          <h3>全屏预览</h3>
          <button @click="closeFullScreen" class="close-btn">
            <X />
          </button>
        </div>
        <iframe
          :srcdoc="generatedContent"
          class="fullscreen-iframe"
          title="全屏网站预览"
        ></iframe>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import {
  Zap, Sparkles, Loader2, Globe, Save, Expand, RefreshCw, 
  Clock, ChevronRight, X
} from 'lucide-vue-next'

const router = useRouter()
const userStore = useUserStore()

const prompt = ref('')
const generatedContent = ref('')
const isGenerating = ref(false)
const showFullScreen = ref(false)
const generationHistory = ref([])

const usageStats = ref({
  used_today: 0,
  remaining_today: 10,
  total_limit: 10
})

// 获取使用统计
const fetchUsageStats = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/ai/usage', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      usageStats.value = await response.json()
    }
  } catch (error) {
    console.error('获取使用统计失败:', error)
  }
}

// 生成网站
const generateWebsite = async () => {
  if (!prompt.value.trim() || usageStats.value.remaining_today <= 0) return
  
  isGenerating.value = true
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/ai/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        prompt: prompt.value.trim()
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      generatedContent.value = result.content
      usageStats.value.remaining_today = result.remaining_uses
      usageStats.value.used_today = usageStats.value.total_limit - result.remaining_uses
      
      // 刷新历史记录
      await fetchHistory()
    } else {
      const error = await response.json()
      alert(error.detail || '生成失败，请重试')
    }
  } catch (error) {
    console.error('生成网站失败:', error)
    alert('网络错误，请检查连接后重试')
  } finally {
    isGenerating.value = false
  }
}

// 获取生成历史
const fetchHistory = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/ai/history', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      generationHistory.value = await response.json()
    }
  } catch (error) {
    console.error('获取历史记录失败:', error)
  }
}

// 选择历史记录
const selectHistory = async (item) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/ai/history/${item.id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      const fullItem = await response.json()
      generatedContent.value = fullItem.generated_content
      prompt.value = fullItem.prompt
    }
  } catch (error) {
    console.error('加载历史记录失败:', error)
  }
}

// 保存为文件
const saveAsFile = () => {
  if (!generatedContent.value) return
  
  const blob = new Blob([generatedContent.value], { type: 'text/html' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `generated-website-${Date.now()}.html`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// 全屏预览
const viewFullScreen = () => {
  showFullScreen.value = true
}

const closeFullScreen = () => {
  showFullScreen.value = false
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  const minutes = Math.floor(diff / (1000 * 60))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN')
}

// 页面初始化
onMounted(async () => {
  await fetchUsageStats()
  await fetchHistory()
})
</script>

<style scoped>
.ai-generator {
  min-height: 95vh;
  background: #f8fafc;
}

.generator-header {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 2rem 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.title-icon {
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.title-section h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.title-section p {
  color: #64748b;
  margin: 0.25rem 0 0 0;
}

/* 使用统计 */
.usage-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.5rem;
}

.usage-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.usage-label {
  color: #64748b;
  font-size: 0.9rem;
}

.usage-value {
  font-weight: 600;
  color: #1e293b;
}

.usage-progress {
  width: 150px;
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #22c55e, #16a34a);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.remaining-text {
  font-size: 0.8rem;
  color: #22c55e;
  font-weight: 500;
}

/* 主要内容区域 */
.generator-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

/* 生成区域 */
.generate-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.card-header {
  margin-bottom: 2rem;
}

.card-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.card-header p {
  color: #64748b;
  margin: 0;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.75rem;
  font-size: 1rem;
  line-height: 1.6;
  resize: vertical;
  transition: border-color 0.3s ease;
}

.form-group textarea:focus {
  outline: none;
  border-color: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

.form-group textarea:disabled {
  background: #f9fafb;
  color: #6b7280;
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.generate-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 25px rgba(34, 197, 94, 0.3);
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(34, 197, 94, 0.4);
}

.generate-btn:disabled {
  background: #d1d5db;
  color: #9ca3af;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.limit-warning {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  border: 1px solid rgba(239, 68, 68, 0.2);
  text-align: center;
}

/* 历史记录 */
.history-section {
  margin-top: 2rem;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.history-header h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #64748b;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.refresh-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.history-list {
  max-height: 300px;
  overflow-y: auto;
}

.empty-history {
  text-align: center;
  padding: 2rem;
  color: #64748b;
}

.empty-icon {
  width: 2.5rem;
  height: 2.5rem;
  margin: 0 auto 0.5rem;
  color: #cbd5e1;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 0.5rem;
  border: 1px solid transparent;
}

.history-item:hover {
  background: #f8fafc;
  border-color: #e2e8f0;
}

.history-content {
  flex: 1;
}

.history-prompt {
  font-size: 0.9rem;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.history-time {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

.history-arrow {
  width: 1rem;
  height: 1rem;
  color: #cbd5e1;
}

/* 预览区域 */
.preview-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.preview-header h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.preview-actions {
  display: flex;
  gap: 0.5rem;
}

.save-btn, .fullscreen-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #64748b;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.save-btn:hover, .fullscreen-btn:hover {
  background: #f1f5f9;
  color: #22c55e;
  border-color: rgba(34, 197, 94, 0.3);
}

.preview-container {
  height: 600px;
  position: relative;
}

.preview-placeholder, .loading-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #64748b;
}

.placeholder-icon {
  width: 4rem;
  height: 4rem;
  margin-bottom: 1rem;
  color: #cbd5e1;
}

.loading-preview h4 {
  font-size: 1.2rem;
  margin: 1rem 0 0.5rem 0;
  color: #1e293b;
}

.loading-animation {
  width: 4rem;
  height: 4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border-radius: 50%;
  color: white;
  margin-bottom: 1rem;
}

.loading-icon {
  width: 2rem;
  height: 2rem;
  animation: spin 1s linear infinite;
}

.preview-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* 全屏预览弹窗 */
.fullscreen-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.fullscreen-content {
  width: 95%;
  height: 95%;
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.fullscreen-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: white;
}

.fullscreen-header h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.fullscreen-iframe {
  flex: 1;
  width: 100%;
  border: none;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .generator-container {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1.5rem;
    align-items: center;
    text-align: center;
  }
}

@media (max-width: 768px) {
  .generator-container {
    padding: 1rem;
  }
  
  .generate-card {
    padding: 1.5rem;
  }
  
  .preview-container {
    height: 400px;
  }
  
  .fullscreen-content {
    width: 98%;
    height: 98%;
  }
  
  .usage-stats {
    align-items: center;
  }
  
  .usage-progress {
    width: 200px;
  }
}
</style>