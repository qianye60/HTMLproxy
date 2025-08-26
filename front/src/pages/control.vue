<template>
  <div class="file-manager">
    <!-- 用户头部区域 -->
    <div class="header-section">
      <div class="container">
        <div class="header-content">
          <div class="page-title">
            <LayoutDashboard class="title-icon" />
            控制面板
          </div>
          <div class="user-profile">
            <div class="user-avatar">
              <User class="user-avatar-icon" />
            </div>
            <div class="user-details">
              <div class="username">{{ userStore.userInfo.username }}</div>
              <div class="user-email">{{ userStore.userInfo.email }}</div>
            </div>
            <button v-if="userStore.userInfo?.is_admin" @click="goToAdmin" class="admin-btn" title="管理面板">
              <Settings class="admin-icon" />
              <span>管理</span>
            </button>
            <button class="logout-btn" @click="showLogoutConfirm = true" title="退出登录">
              <LogOut class="logout-icon" />
              <span>退出</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-section">
  <div class="container">
    <div class="stats-grid">
      <!-- 文件总数卡片 -->
      <div class="stat-card">
        <div class="stat-icon" style="background-color: #dbeafe; color: #3b82f6;">
          <!-- 文件图标 SVG -->
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
            <rect x="4" y="4" width="16" height="16" rx="2" fill="#dbeafe"/>
            <path d="M8 8h8M8 12h8M8 16h4" stroke="#3b82f6" stroke-width="2" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-label">文件总数</div>
          <div class="stat-value">{{ userStore.statCards[0].value }}</div>
        </div>
      </div>
      <!-- 已用空间卡片 -->
      <div class="stat-card">
        <div class="stat-icon" style="background-color: #dcfce7; color: #10b981;">
          <!-- 数据库/存储图标 SVG -->
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
            <ellipse cx="12" cy="6" rx="8" ry="3" fill="#dcfce7"/>
            <ellipse cx="12" cy="6" rx="8" ry="3" stroke="#10b981" stroke-width="2"/>
            <path d="M4 6v6c0 1.66 3.58 3 8 3s8-1.34 8-3V6" stroke="#10b981" stroke-width="2"/>
            <path d="M4 12v6c0 1.66 3.58 3 8 3s8-1.34 8-3v-6" stroke="#10b981" stroke-width="2"/>
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-label">已用空间</div>
          <div class="stat-value">{{ userStore.statCards[1].value }}</div>
        </div>
      </div>
    </div>
  </div>
</div>

    <!-- 操作与拖拽上传区域 -->
    <div class="actions-section">
      <div class="container">
        <div 
          class="upload-area"
          :class="{ 'drag-over': isDragOver }"
          @dragover.prevent="isDragOver = true"
          @dragleave.prevent="isDragOver = false"
          @drop.prevent="handleDrop"
        >
          <div class="upload-icon-wrapper">
            <UploadCloud class="upload-area-icon" />
          </div>
          <h3 class="upload-title">拖拽文件到这里，或点击按钮上传</h3>
          <div class="upload-buttons">
            <button 
              class="upload-btn"
              @click="handleUpload"
              :disabled="userStore.isUploading"
            >
              <FileUp class="btn-icon" />
              {{ userStore.isUploading ? '上传中...' : '上传新文件' }}
            </button>
            <button 
              class="paste-btn"
              @click="showPasteModal = true"
              :disabled="userStore.isUploading"
            >
              <ClipboardPaste class="btn-icon" />
              粘贴HTML代码
            </button>
            <button 
              class="ai-btn"
              @click="showAIGenModal = true"
              :disabled="userStore.isUploading"
            >
              <Sparkles class="btn-icon" />
              AI生成HTML
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 文件列表区域 -->
    <div class="files-section">
      <div class="container">
        <div class="files-card">
          <div class="card-header">
            <h3 class="card-title">
              <List class="title-icon" />
              我的HTML文件
            </h3>
            <div class="file-count">共 {{ userStore.files.length }} 个文件</div>
          </div>
          
          <div class="files-table-container">
            <table class="files-table">
              <thead>
                <tr>
                  <th>项目名称</th>
                  <th>文件名</th>
                  <th>文件大小</th>
                  <th>上传时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="file in userStore.files" :key="file.id" class="file-row">
                  <td class="project-name-cell">
                    <div class="project-info">
                      <div class="project-avatar">
                        {{ file.projectName.charAt(0).toUpperCase() }}
                      </div>
                      <div v-if="!file.editing" class="project-name">
                        {{ file.projectName }}
                      </div>
                      <input 
                        v-else
                        v-model="file.editProjectName"
                        class="project-input"
                        @keyup.enter="saveProjectName(file)"
                        @keyup.esc="cancelEditProjectName(file)"
                        @blur="saveProjectName(file)"
                        ref="editInput"
                      />
                      <button 
                        v-if="!file.editing"
                        class="edit-btn"
                        @click="editProjectName(file)"
                        title="编辑项目名"
                      >
                        <Pencil class="edit-icon" />
                      </button>
                    </div>
                  </td>
                  
                  <td class="filename-cell">
                    <a :href="getFileUrl(file.url)" target="_blank" class="file-link">
                      <FileText class="file-icon" />
                      {{ file.filename }}
                    </a>
                  </td>
                  
                  <td class="size-cell">
                    <span class="size-badge">{{ file.size }}</span>
                  </td>
                  
                  <td class="time-cell">
                    <span class="upload-time">{{ formatTime(file.uploadTime) }}</span>
                  </td>
                  
                  <td class="actions-cell">
                    <div class="action-buttons">
                      <a 
                        :href="getFileUrl(file.url)" 
                        target="_blank" 
                        class="action-btn view-btn"
                        title="查看文件"
                      >
                        <ExternalLink class="action-icon" />
                      </a>
                      <button 
                        class="action-btn delete-btn"
                        @click="deleteFile(file)"
                        title="删除文件"
                      >
                        <Trash2 class="action-icon" />
                      </button>
                    </div>
                  </td>
                </tr>
                
                <tr v-if="userStore.files.length === 0" class="empty-row">
                  <td colspan="5" class="empty-cell">
                    <div class="empty-state">
                      <FolderOpen class="empty-icon" />
                      <p>暂无文件，点击上方按钮上传您的第一个文件</p>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    
    <!-- HTML代码粘贴弹窗 -->
    <div v-if="showPasteModal" class="modal-overlay" @click="closePasteModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">
            <ClipboardPaste class="modal-icon" />
            粘贴HTML代码
          </h3>
          <button class="close-btn" @click="closePasteModal">
            <X class="close-icon" />
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="project-name">项目名称</label>
            <input 
              id="project-name"
              v-model="pasteForm.projectName"
              type="text"
              placeholder="请输入项目名称"
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="html-code">HTML代码</label>
            <textarea 
              id="html-code"
              v-model="pasteForm.htmlCode"
              placeholder="请粘贴您的HTML代码..."
              class="form-textarea"
              rows="12"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closePasteModal">取消</button>
          <button 
            class="submit-btn"
            @click="handlePasteUpload"
            :disabled="!pasteForm.projectName.trim() || !pasteForm.htmlCode.trim() || userStore.isUploading"
          >
            {{ userStore.isUploading ? '上传中...' : '上传' }}
          </button>
        </div>
      </div>
    </div>

    <!-- AI生成等待弹窗 -->
    <div v-if="showAILoadingModal" class="modal-overlay">
      <div class="loading-modal" @click.stop>
        <div class="loading-content">
          <div class="loading-spinner">
            <div class="spinner"></div>
          </div>
          <h3 class="loading-title">AI正在生成中...</h3>
          <p class="loading-subtitle">请耐心等待，通常需要10-30秒</p>
        </div>
      </div>
    </div>

    <!-- AI生成HTML弹窗 -->
    <div v-if="showAIGenModal" class="modal-overlay" @click="closeAIGenModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">
            <Sparkles class="modal-icon" />
            AI生成HTML
          </h3>
          <button class="close-btn" @click="closeAIGenModal">
            <X class="close-icon" />
          </button>
        </div>
        <div class="modal-body">
          <!-- 使用统计显示 -->
          <div class="usage-stats-display">
            <div class="usage-item">
              <span class="usage-label">今日已用：</span>
              <span class="usage-value">{{ usageStats.used_today }}/{{ usageStats.total_limit }}</span>
            </div>
            <div class="usage-item">
              <span class="usage-label">剩余次数：</span>
              <span class="usage-remaining">{{ usageStats.remaining_today }}</span>
            </div>
          </div>
          
          <textarea
            v-model="aiPrompt"
            placeholder="请详细描述您想要生成的网站，例如：创建一个现代化的个人博客首页，包含导航栏、文章列表、侧边栏和页脚"
            class="form-textarea"
            rows="8"
          ></textarea>
          <div v-if="aiHtml" class="ai-html-preview">
            <label>生成结果预览：</label>
            <iframe :srcdoc="aiHtml" class="ai-html-iframe"></iframe>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeAIGenModal">取消</button>
          <button class="submit-btn" @click="handleAIGenerate" :disabled="!aiPrompt || usageStats.remaining_today <= 0 || showAILoadingModal">
            {{ showAILoadingModal ? '生成中...' : (usageStats.remaining_today <= 0 ? '今日次数已用完' : '生成HTML') }}
          </button>
          <button v-if="aiHtml" class="submit-btn" @click="uploadAIGeneratedHtml">一键上传</button>
          <button v-if="aiHtml" class="submit-btn" @click="downloadAIGeneratedHtml">下载HTML</button>
        </div>
      </div>
    </div>

    <!-- 退出确认弹窗 -->
    <div v-if="showLogoutConfirm" class="dialog-mask">
      <div class="dialog">
        <h3>确认退出登录？</h3>
        <div class="dialog-actions">
          <button @click="confirmLogout" class="dialog-btn danger">确定</button>
          <button @click="showLogoutConfirm = false" class="dialog-btn">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { 
  LayoutDashboard, User, LogOut, FileUp, ClipboardPaste, List, 
  Pencil, FileText, ExternalLink, Trash2, FolderOpen, X, UploadCloud, Sparkles, Settings
} from 'lucide-vue-next'

const editInput = ref<HTMLInputElement[]>([])
const userStore = useUserStore()
const router = useRouter()
const isDragOver = ref(false)

// 粘贴弹窗相关
const showPasteModal = ref(false)
const pasteForm = ref({
  projectName: '',
  htmlCode: ''
})

// 退出确认弹窗
const showLogoutConfirm = ref(false)
const confirmLogout = () => {
  showLogoutConfirm.value = false
  handleLogout()
}

// AI生成HTML弹窗相关
const showAIGenModal = ref(false)
const showAILoadingModal = ref(false)
const aiPrompt = ref('')
const aiHtml = ref('')

// 使用统计数据
const usageStats = ref({
  used_today: 0,
  remaining_today: 10,
  total_limit: 10
})

// 获取使用统计
const fetchUsageStats = async () => {
  try {
    const token = localStorage.getItem('JWTtoken')
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

const closeAIGenModal = () => {
  showAIGenModal.value = false
  aiPrompt.value = ''
  aiHtml.value = ''
}

const handleAIGenerate = async () => {
  if (!aiPrompt.value.trim() || usageStats.value.remaining_today <= 0) return
  
  // 显示等待弹窗
  showAILoadingModal.value = true
  aiHtml.value = ''
  
  try {
    const token = localStorage.getItem('JWTtoken')
    const res = await fetch('/api/ai/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        prompt: aiPrompt.value.trim()
      })
    })
    
    if (res.ok) {
      const data = await res.json()
      aiHtml.value = data.content
      // 更新剩余次数
      usageStats.value.remaining_today = data.remaining_uses
      usageStats.value.used_today = usageStats.value.total_limit - data.remaining_uses
    } else {
      const error = await res.json()
      alert(error.detail || '生成失败，请重试')
    }
  } catch (e) {
    alert('生成失败，请检查网络连接')
  } finally {
    showAILoadingModal.value = false
  }
}

const uploadAIGeneratedHtml = async () => {
  if (!aiHtml.value) return
  const blob = new Blob([aiHtml.value], { type: 'text/html' })
  const file = new File([blob], 'ai-generated.html', { type: 'text/html' })
  await uploadFileFlow(file)
  closeAIGenModal()
}

const downloadAIGeneratedHtml = () => {
  if (!aiHtml.value) return
  const blob = new Blob([aiHtml.value], { type: 'text/html' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = 'ai-generated.html'
  a.click()
  URL.revokeObjectURL(url)
}

// 页面加载时自动初始化数据
onMounted(async () => {
  const loginStatus = await userStore.checkLoginStatus()
  if (loginStatus.islogin) {
    await userStore.initializeData()
    await fetchUsageStats()  // 获取AI使用统计
  }
})

// 工具函数
const formatTime = (timeStr: string): string => {
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 7) return `${days}天前`
  return timeStr.split(' ')[0]
}

const handleDrop = (event: DragEvent) => {
  isDragOver.value = false;
  const file = event.dataTransfer?.files[0];
  if (file) {
    uploadFileFlow(file);
  }
};

const uploadFileFlow = async (file: File) => {
  if (userStore.isUploading) return;
  try {
    userStore.isUploading = true
    await userStore.uploadFile(file)
  } catch (err) {
    alert('上传失败，请重试')
  } finally {
    userStore.isUploading = false
  }
}

// 上传文件
const handleUpload = async () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.html,.htm'
  input.onchange = async (e) => {
    const file = (e.target as HTMLInputElement).files?.[0]
    if (file) {
      await uploadFileFlow(file)
    }
  }
  input.click()
}

// 编辑项目名
const editProjectName = async (file: any) => {
  file.editing = true
  file.editProjectName = file.projectName
  await nextTick()
  const input = editInput.value?.find(el => el)
  input?.focus()
}

const saveProjectName = async (file: any) => {
  if (!file.editing) return;
  if (!file.editProjectName.trim()) {
    alert('项目名不能为空')
    return
  }
  try {
    const success = await userStore.updateProjectName(file.id, file.editProjectName.trim())
    if (success) {
      file.projectName = file.editProjectName.trim()
      file.editing = false
    } else {
      throw new Error('更新失败')
    }
  } catch (error) {
    alert('更新失败，请重试')
  }
}

const cancelEditProjectName = (file: any) => {
  file.editing = false
  file.editProjectName = ''
}

const deleteFile = async (file: any) => {
  if (!confirm(`确定要删除文件 "${file.filename}" 吗？删除后不可恢复`)) {
    return
  }
  try {
    await userStore.deleteFile(file.id)
  } catch (error) {
    alert('删除失败，请重试')
  }
}

// 粘贴弹窗相关功能
const closePasteModal = () => {
  showPasteModal.value = false
  pasteForm.value = {
    projectName: '',
    htmlCode: ''
  }
}

const handlePasteUpload = async () => {
  if (!pasteForm.value.projectName.trim() || !pasteForm.value.htmlCode.trim()) {
    alert('请填写项目名称和HTML代码')
    return
  }
  
  const blob = new Blob([pasteForm.value.htmlCode], { type: 'text/html' })
  const file = new File([blob], `${pasteForm.value.projectName}.html`, { type: 'text/html' })
  await uploadFileFlow(file)
  if (!userStore.isUploading) {
    closePasteModal()
  }
}

const handleLogout = () => {
  userStore.logout();
  router.push('/login');
}

const goToAdmin = () => {
  router.push('/admin')
}

// 处理文件URL，确保在生产环境中使用正确的端口
const getFileUrl = (url: string): string => {
  // 如果URL已经是完整的绝对路径，直接返回
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  // 如果是相对路径且当前页面是通过40000端口访问的，重定向到8080端口
  if (url.startsWith('/html/') && window.location.port === '40000') {
    return window.location.protocol + '//' + window.location.hostname + ':8080' + url
  }
  // 默认情况下直接返回相对路径，让浏览器基于当前页面解析
  return url
}

// 组件图标 (从您原有的代码中保留，以确保 userStore.statCards 能正常工作)
const FileIcon = {
  template: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/></svg>`
}
const StorageIcon = {
  template: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6,2H18A2,2 0 0,1 20,4V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V4A2,2 0 0,1 6,2M12,4A6,6 0 0,0 6,10C6,13.31 8.69,16 12.1,16L11.22,18.18C11.5,18.69 12.07,19 12.66,19H14.66C15.25,19 15.82,18.69 16.1,18.18L15.22,16C18.53,16 21.22,13.31 21.22,10A6,6 0 0,0 12,4Z"/></svg>`
}
</script>

<style scoped>
/* 全局样式 */
.file-manager {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 头部区域 */
.header-section {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(8px);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
}

.page-title {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

.title-icon {
  width: 28px;
  height: 28px;
  color: #3b82f6;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background: #dbeafe;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
}

.user-avatar-icon {
  width: 20px;
  height: 20px;
}

.username {
  font-weight: 600;
  color: #1e293b;
  font-size: 16px;
}

.user-email {
  font-size: 14px;
  color: #64748b;
}

.admin-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #e0f2fe;
  color: #0284c7;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  font-size: 14px;
}
.admin-btn:hover {
  background: #bae6fd;
  color: #0369a1;
}
.admin-icon {
  width: 16px;
  height: 16px;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #fee2e2;
  color: #ef4444;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}
.logout-btn:hover {
  background: #fecaca;
  color: #dc2626;
}
.logout-icon {
  width: 16px;
  height: 16px;
}

/* 统计区域 */
.stats-section {
  padding: 32px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.05);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon :deep(svg) {
  width: 24px;
  height: 24px;
}

.stat-label {
  font-size: 14px;
  color: #64748b;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
}

/* 操作区域 */
.actions-section {
  padding: 0 0 32px 0;
}

.upload-area {
  border: 2px dashed #cbd5e1;
  border-radius: 1rem;
  padding: 2rem;
  text-align: center;
  background-color: white;
  transition: 全部 0.3s ease;
}
.upload-area.drag-over {
  border-color: #3b82f6;
  background-color: #eff6ff;
}
.upload-icon-wrapper {
  width: 4rem;
  height: 4rem;
  background-color: #f1f5f9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}
.upload-area-icon {
  width: 2rem;
  height: 2rem;
  color: #64748b;
}
.upload-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #334155;
  margin-bottom: 1rem;
}

.upload-btn, .paste-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: 全部 0.2s;
  box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.3);
}

.upload-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px 0 rgba(59, 130, 246, 0.4);
}

.upload-btn:disabled, .paste-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-icon {
  width: 20px;
  height: 20px;
}

.upload-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.paste-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.3);
}

.paste-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px 0 rgba(16, 185, 129, 0.4);
}

.ai-btn {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e42 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 14px 0 rgba(251, 191, 36, 0.3);
  margin-left: 8px;
}
.ai-btn:hover:not(:disabled) {
  background: #f59e42;
}

/* 弹窗样式 (保持您原有的样式) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}
.modal-content {
  background: white;
  border-radius: 16px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #e2e8f0;
  flex-shrink: 0;
}
.modal-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}
.modal-icon {
  width: 24px;
  height: 24px;
  color: #10b981;
}
.close-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 4px;
  border-radius: 50%;
  transition: 全部 0.2s;
}
.close-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}
.close-icon {
  width: 20px;
  height: 20px;
}
.modal-body {
  padding: 24px;
  overflow-y: auto;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #374151;
}
.form-input, .form-textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-sizing: border-box;
}
.form-input:focus, .form-textarea:focus {
  border-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}
.form-textarea {
  resize: vertical;
  min-height: 240px;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  line-height: 1.5;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 24px;
  border-top: 1px solid #e2e8f0;
  background: #f8fafc;
  flex-shrink: 0;
}
.cancel-btn {
  background: white;
  color: #64748b;
  border: 1px solid #e2e8f0;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: 全部 0.2s;
}
.cancel-btn:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}
.submit-btn {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: 全部 0.2s;
  box-shadow: 0 4px 14px 0 rgba(16, 185, 129, 0.39);
}
.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 25px 0 rgba(16, 185, 129, 0.5);
}
.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 文件列表区域 (保持您原有的样式) */
.files-section {
  padding-bottom: 40px;
}
.files-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}
.card-header {
  padding: 24px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}
.file-count {
  font-size: 14px;
  color: #64748b;
  background: #f1f5f9;
  padding: 4px 12px;
  border-radius: 20px;
}
.files-table-container {
  overflow-x: auto;
}
.files-table {
  width: 100%;
  border-collapse: collapse;
}
.files-table th {
  background: #f8fafc;
  padding: 16px 24px;
  text-align: left;
  font-weight: 600;
  color: #475569;
  font-size: 14px;
  border-bottom: 1px solid #e2e8f0;
}
.file-row {
  transition: background-color 0.2s;
}
.file-row:hover {
  background: #f8fafc;
}
.files-table td {
  padding: 16px 24px;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}
.project-info {
  display: flex;
  align-items: center;
  gap: 12px;
}
.project-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}
.project-name {
  font-weight: 500;
  color: #1e293b;
}
.project-input {
  border: 2px solid #3b82f6;
  border-radius: 6px;
  padding: 4px 8px;
  font-size: 14px;
  outline: none;
  min-width: 120px;
}
.edit-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: 全部 0.2s;
}
.edit-btn:hover {
  background: #f1f5f9;
  color: #3b82f6;
}
.edit-icon {
  width: 16px;
  height: 16px;
}
.file-link {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #3b82f6;
  font-weight: 500;
  transition: color 0.2s;
}
.file-link:hover {
  color: #1d4ed8;
}
.file-icon {
  width: 20px;
  height: 20px;
}
.size-badge {
  background: #f1f5f9;
  color: #475569;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 500;
}
.upload-time {
  color: #64748b;
  font-size: 14px;
}
.action-buttons {
  display: flex;
  gap: 8px;
}
.action-btn {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 全部 0.2s;
  text-decoration: none;
}
.action-icon {
  width: 16px;
  height: 16px;
}
.view-btn {
  background: #dbeafe;
  color: #3b82f6;
}
.view-btn:hover {
  background: #bfdbfe;
}
.delete-btn {
  background: #fee2e2;
  color: #ef4444;
}
.delete-btn:hover {
  background: #fecaca;
}
.empty-row td {
  border: none;
}
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #64748b;
}
.empty-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 16px;
  color: #cbd5e1;
}
.empty-state p {
  margin: 0;
  font-size: 16px;
}

.ai-html-preview {
  margin-top: 16px;
}
.ai-html-iframe {
  width: 100%;
  min-height: 200px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
}

/* AI等待弹窗样式 */
.loading-modal {
  background: white;
  border-radius: 20px;
  padding: 3rem 2rem;
  max-width: 400px;
  width: 90%;
  text-align: center;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
  border: 1px solid #e2e8f0;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.loading-spinner {
  position: relative;
  width: 80px;
  height: 80px;
}

.spinner {
  width: 80px;
  height: 80px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #22c55e;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.loading-subtitle {
  color: #64748b;
  margin: 0;
  font-size: 1rem;
}

/* 使用统计显示样式 */
.usage-stats-display {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.usage-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.usage-label {
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
}

.usage-value {
  color: #1e293b;
  font-weight: 600;
  font-size: 14px;
}

.usage-remaining {
  color: #22c55e;
  font-weight: 600;
  font-size: 14px;
  background: rgba(34, 197, 94, 0.1);
  padding: 4px 8px;
  border-radius: 6px;
}

/* 退出确认弹窗 (保持您原有的样式) */
.dialog-mask {
  position: fixed;
  z-index: 1000;
  left: 0; top: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.25);
  display: flex;
  align-items: center;
  justify-content: center;
}
.dialog {
  background: #fff;
  border-radius: 12px;
  padding: 32px 24px 24px 24px;
  min-width: 260px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  gap: 16px;
  align-items: center;
}
.dialog-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}
.dialog-btn {
  padding: 8px 20px;
  border-radius: 6px;
  border: none;
  background: #3b82f6;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.dialog-btn.danger {
  background: #ef4444;
}
.dialog-btn:active {
  background: #2563eb;
}

/* 响应式设计 (保持您原有的样式) */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  .stats-grid {
    grid-template-columns: 1fr;
  }
  .files-table-container {
    font-size: 14px;
  }
  .files-table th,
  .files-table td {
    padding: 12px 16px;
  }
  .project-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  .action-buttons {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 16px;
  }
  .page-title {
    font-size: 24px;
  }
  .upload-btn, .paste-btn {
    padding: 12px 24px;
    font-size: 14px;
  }
}
</style>