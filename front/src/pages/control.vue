<template>
    <div class="file-manager">
      <!-- 用户头部区域 -->
      <div class="header-section">
        <div class="container">
          <div class="header-content">
            <div class="page-title">
              <svg class="title-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
              </svg>
              控制面板
            </div>
            <div class="user-profile">
              <div class="user-avatar">
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
              </div>
              <div class="user-details">
                <div class="username">{{ userStore.userInfo.username }}</div>
                <div class="user-email">{{ userStore.userInfo.email }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- 统计卡片区域 -->
      <div class="stats-section">
        <div class="container">
          <div class="stats-grid">
            <div 
              v-for="card in userStore.statCards" 
              :key="card.id"
              class="stat-card"
            >
              <div class="stat-icon" :style="{ backgroundColor: card.color, color: card.iconColor }">
                <component :is="card.icon" />
              </div>
              <div class="stat-content">
                <div class="stat-label">{{ card.label }}</div>
                <div class="stat-value">{{ card.value }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- 操作区域 -->
      <div class="actions-section">
        <div class="container">
          <button 
            class="upload-btn"
            @click="handleUpload"
            :disabled="userStore.isUploading"
          >
            <svg class="btn-icon" viewBox="0 0 24 24" fill="currentColor">
              <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
            </svg>
            {{ userStore.isUploading ? '上传中...' : '上传新文件' }}
          </button>
        </div>
      </div>
  
      <!-- 文件列表区域 -->
      <div class="files-section">
        <div class="container">
          <div class="files-card">
            <div class="card-header">
              <h3 class="card-title">
                <svg class="title-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M6,2A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2H6Z"/>
                </svg>
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
                    <!-- 项目名称列 -->
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
                          <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"/>
                          </svg>
                        </button>
                      </div>
                    </td>
                    
                    <!-- 文件名列 -->
                    <td class="filename-cell">
                      <a :href="file.url" target="_blank" class="file-link">
                        <div class="file-icon">
                          <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                          </svg>
                        </div>
                        {{ file.filename }}
                      </a>
                    </td>
                    
                    <!-- 文件大小列 -->
                    <td class="size-cell">
                      <span class="size-badge">{{ file.size }}</span>
                    </td>
                    
                    <!-- 上传时间列 -->
                    <td class="time-cell">
                      <span class="upload-time">{{ formatTime(file.uploadTime) }}</span>
                    </td>
                    
                    <!-- 操作列 -->
                    <td class="actions-cell">
                      <div class="action-buttons">
                        <a 
                          :href="file.url" 
                          target="_blank" 
                          class="action-btn view-btn"
                          title="查看文件"
                        >
                          <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M12,9A3,3 0 0,0 9,12A3,3 0 0,0 12,15A3,3 0 0,0 15,12A3,3 0 0,0 12,9M12,17A5,5 0 0,1 7,12A5,5 0 0,1 12,7A5,5 0 0,1 17,12A5,5 0 0,1 12,17M12,4.5C7,4.5 2.73,7.61 1,12C2.73,16.39 7,19.5 12,19.5C17,19.5 21.27,16.39 23,12C21.27,7.61 17,4.5 12,4.5Z"/>
                          </svg>
                        </a>
                        <button 
                          class="action-btn delete-btn"
                          @click="deleteFile(file)"
                          title="删除文件"
                        >
                          <svg viewBox="0 0 24 24" fill="currentColor">
                            <path d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"/>
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                  
                  <!-- 空状态 -->
                  <tr v-if="userStore.files.length === 0" class="empty-row">
                    <td colspan="5" class="empty-cell">
                      <div class="empty-state">
                        <svg class="empty-icon" viewBox="0 0 24 24" fill="currentColor">
                          <path d="M13,9H18.5L13,3.5V9M6,2H14L20,8V20A2,2 0 0,1 18,22H6C4.89,22 4,21.1 4,20V4C4,2.89 4.89,2 6,2M15,18V16H6V18H15M18,14V12H6V14H18Z"/>
                        </svg>
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
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, nextTick, onMounted } from 'vue'
  import { useUserStore } from '@/stores/user'

  const editInput = ref<HTMLInputElement[]>([])
  const userStore = useUserStore()

  // 页面加载时自动初始化数据
  onMounted(async () => {
    const loginStatus = await userStore.checkLoginStatus()
    if (loginStatus.islogin) {
      await userStore.initializeData()
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

  // 上传文件
  const handleUpload = async () => {
    try {
      userStore.isUploading = true
      const input = document.createElement('input')
      input.type = 'file'
      input.accept = '.html,.htm'
      input.onchange = async (e) => {
        const file = (e.target as HTMLInputElement).files?.[0]
        if (file) {
          try {
            await userStore.uploadFile(file)
          } catch (err) {
            alert('上传失败，请重试')
          }
        }
      }
      input.click()
    } finally {
      userStore.isUploading = false
    }
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

  // 组件图标
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
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 0;
  }
  
  .page-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 28px;
    font-weight: 700;
    color: #1e293b;
  }
  
  .title-icon {
    width: 32px;
    height: 32px;
    color: #3b82f6;
  }
  
  .user-profile {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #f8fafc;
    padding: 12px 16px;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
  }
  
  .user-avatar {
    width: 40px;
    height: 40px;
    background: #3b82f6;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }
  
  .user-avatar svg {
    width: 24px;
    height: 24px;
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
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    gap: 16px;
    transition: transform 0.2s, box-shadow 0.2s;
  }
  
  .stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px -5px rgba(0, 0, 0, 0.1);
  }
  
  .stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
  }
  
  .stat-icon svg {
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
    text-align: center;
  }
  
  .upload-btn {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    border: none;
    padding: 16px 32px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.2s;
    box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.39);
  }
  
  .upload-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px 0 rgba(59, 130, 246, 0.5);
  }
  
  .upload-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  .btn-icon {
    width: 20px;
    height: 20px;
  }
  
  /* 文件列表区域 */
  .files-section {
    padding-bottom: 40px;
  }
  
  .files-card {
    background: white;
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
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
  
  /* 项目名称单元格 */
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
    transition: all 0.2s;
  }
  
  .edit-btn:hover {
    background: #f1f5f9;
    color: #3b82f6;
  }
  
  .edit-btn svg {
    width: 16px;
    height: 16px;
  }
  
  /* 文件名单元格 */
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
    color: #3b82f6;
  }
  
  /* 文件大小单元格 */
  .size-badge {
    background: #f1f5f9;
    color: #475569;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
  }
  
  /* 时间单元格 */
  .upload-time {
    color: #64748b;
    font-size: 14px;
  }
  
  /* 操作单元格 */
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
    transition: all 0.2s;
    text-decoration: none;
  }
  
  .action-btn svg {
    width: 16px;
    height: 16px;
  }
  
  .view-btn {
    background: #dbeafe;
    color: #3b82f6;
  }
  
  .view-btn:hover {
    background: #bfdbfe;
    color: #1d4ed8;
  }
  
  .delete-btn {
    background: #fee2e2;
    color: #ef4444;
  }
  
  .delete-btn:hover {
    background: #fecaca;
    color: #dc2626;
  }
  
  /* 空状态 */
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
  
  /* 响应式设计 */
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
    
    .upload-btn {
      padding: 12px 24px;
      font-size: 14px;
    }
  }
  </style>
  