<template>
  <div class="admin-panel">
    <div class="admin-header">
      <h1>管理员面板</h1>
      <p>API配置管理</p>
    </div>

    <!-- 统计信息 -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <Zap />
        </div>
        <div class="stat-info">
          <h3>{{ stats.total_generations_today }}</h3>
          <p>今日生成次数</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <Users />
        </div>
        <div class="stat-info">
          <h3>{{ stats.active_users_today }}</h3>
          <p>今日活跃用户</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <Globe />
        </div>
        <div class="stat-info">
          <h3>{{ stats.total_users }}</h3>
          <p>总用户数</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <Settings />
        </div>
        <div class="stat-info">
          <h3>{{ stats.current_daily_limit }}</h3>
          <p>每日生成限制</p>
        </div>
      </div>
    </div>

    <!-- 系统设置 -->
    <div class="config-section">
      <div class="section-header">
        <h2>系统设置</h2>
      </div>
      
      <div class="settings-grid">
        <div class="setting-item">
          <div class="setting-info">
            <h3>每日生成限制</h3>
            <p>设置每个用户每天可以使用AI生成的次数</p>
          </div>
          <div class="setting-control">
            <div class="limit-input-group">
              <input 
                v-model.number="dailyLimitForm.limit" 
                type="number" 
                min="1" 
                max="1000"
                class="limit-input"
              />
              <span class="limit-unit">次/天</span>
              <button 
                @click="updateDailyLimit" 
                :disabled="isUpdatingLimit"
                class="update-btn"
              >
                {{ isUpdatingLimit ? '更新中...' : '更新' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- API配置管理 -->
    <div class="config-section">
      <div class="section-header">
        <h2>API配置管理</h2>
        <button @click="showAddModal = true" class="add-btn">
          <Plus />
          添加配置
        </button>
      </div>

      <div class="config-list">
        <div v-if="apiConfigs.length === 0" class="empty-state">
          <Server class="empty-icon" />
          <h3>暂无API配置</h3>
          <p>请添加第一个API配置以启用AI生成功能</p>
        </div>

        <div v-for="config in apiConfigs" :key="config.id" class="config-item">
          <div class="config-info">
            <div class="config-header">
              <h3>{{ config.name }}</h3>
              <div class="config-status">
                <div :class="['status-badge', config.is_active ? 'active' : 'inactive']">
                  {{ config.is_active ? '启用' : '禁用' }}
                </div>
              </div>
            </div>
            <div class="config-details">
              <p><strong>模型:</strong> {{ config.model }}</p>
              <p><strong>API地址:</strong> {{ config.base_url }}</p>
              <p><strong>API Key:</strong> {{ config.api_key }}</p>
              <p><strong>创建时间:</strong> {{ formatDate(config.created_time) }}</p>
            </div>
          </div>
          <div class="config-actions">
            <button @click="editConfig(config)" class="edit-btn">
              <Edit />
              编辑
            </button>
            <button @click="deleteConfig(config.id)" class="delete-btn">
              <Trash2 />
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑配置弹窗 -->
    <div v-if="showAddModal || editingConfig" class="modal-overlay" @click="closeModal">
      <div class="modal" @click.stop>
        <div class="modal-header">
          <h3>{{ editingConfig ? '编辑API配置' : '添加API配置' }}</h3>
          <button @click="closeModal" class="close-btn">
            <X />
          </button>
        </div>
        
        <form @submit.prevent="submitConfig" class="modal-body">
          <div class="form-group">
            <label>配置名称</label>
            <input
              v-model="configForm.name"
              type="text"
              placeholder="如: OpenAI GPT-4"
              required
            />
          </div>
          
          <div class="form-group">
            <label>API基础URL</label>
            <input
              v-model="configForm.base_url"
              type="url"
              placeholder="https://api.openai.com"
              required
            />
          </div>
          
          <div class="form-group">
            <label>模型名称</label>
            <input
              v-model="configForm.model"
              type="text"
              placeholder="gpt-4"
              required
            />
          </div>
          
          <div class="form-group">
            <label>API Key</label>
            <input
              v-model="configForm.api_key"
              type="password"
              placeholder="sk-..."
              required
            />
          </div>
          
          <div class="form-group" v-if="editingConfig">
            <label class="checkbox-label">
              <input
                v-model="configForm.is_active"
                type="checkbox"
              />
              启用此配置
            </label>
          </div>
        </form>
        
        <div class="modal-footer">
          <button @click="closeModal" class="cancel-btn">取消</button>
          <button @click="submitConfig" class="submit-btn">
            {{ editingConfig ? '更新' : '添加' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import {
  Zap, Users, Globe, Settings, Plus, Server, Edit, Trash2, X
} from 'lucide-vue-next'

const router = useRouter()
const userStore = useUserStore()

const stats = ref({
  total_generations_today: 0,
  active_users_today: 0,
  total_users: 0,
  current_daily_limit: 10
})

const dailyLimitForm = ref({
  limit: 10
})

const isUpdatingLimit = ref(false)

const apiConfigs = ref([])
const showAddModal = ref(false)
const editingConfig = ref(null)
const configForm = ref({
  name: '',
  base_url: '',
  model: '',
  api_key: '',
  is_active: true
})

// 检查管理员权限
const checkAdminAccess = () => {
  if (!userStore.userInfo?.is_admin) {
    router.push('/home')
    return false
  }
  return true
}

// 获取统计数据
const fetchStats = async () => {
  try {
    const token = localStorage.getItem('JWTtoken')
    const response = await fetch('/api/ai/admin/usage-stats', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      stats.value = await response.json()
      // 同步更新表单
      dailyLimitForm.value.limit = stats.value.current_daily_limit
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 更新每日限制
const updateDailyLimit = async () => {
  if (!dailyLimitForm.value.limit || dailyLimitForm.value.limit < 1) {
    alert('请输入有效的限制次数')
    return
  }
  
  isUpdatingLimit.value = true
  
  try {
    const token = localStorage.getItem('JWTtoken')
    const response = await fetch(`/api/ai/admin/daily-limit?limit=${dailyLimitForm.value.limit}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      const result = await response.json()
      alert(result.message || '更新成功')
      // 刷新统计数据
      await fetchStats()
    } else {
      const error = await response.json()
      alert(error.detail || '更新失败')
    }
  } catch (error) {
    console.error('更新每日限制失败:', error)
    alert('网络错误，请重试')
  } finally {
    isUpdatingLimit.value = false
  }
}

// 获取API配置列表
const fetchApiConfigs = async () => {
  try {
    const token = localStorage.getItem('JWTtoken')
    const response = await fetch('/api/ai/admin/api-configs', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      apiConfigs.value = await response.json()
    }
  } catch (error) {
    console.error('获取API配置失败:', error)
  }
}

// 提交配置
const submitConfig = async () => {
  try {
    const token = localStorage.getItem('JWTtoken')
    const url = editingConfig.value 
      ? `/api/ai/admin/api-configs/${editingConfig.value.id}`
      : '/api/ai/admin/api-configs'
    
    const method = editingConfig.value ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(configForm.value)
    })
    
    if (response.ok) {
      closeModal()
      await fetchApiConfigs()
    } else {
      const error = await response.json()
      alert(error.detail || '操作失败')
    }
  } catch (error) {
    console.error('提交配置失败:', error)
    alert('网络错误，请重试')
  }
}

// 编辑配置
const editConfig = (config) => {
  editingConfig.value = config
  configForm.value = {
    name: config.name,
    base_url: config.base_url,
    model: config.model,
    api_key: '',
    is_active: config.is_active
  }
}

// 删除配置
const deleteConfig = async (id) => {
  if (!confirm('确定要删除此配置吗？')) return
  
  try {
    const token = localStorage.getItem('JWTtoken')
    const response = await fetch(`/api/ai/admin/api-configs/${id}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    if (response.ok) {
      await fetchApiConfigs()
    } else {
      const error = await response.json()
      alert(error.detail || '删除失败')
    }
  } catch (error) {
    console.error('删除配置失败:', error)
    alert('网络错误，请重试')
  }
}

// 关闭弹窗
const closeModal = () => {
  showAddModal.value = false
  editingConfig.value = null
  configForm.value = {
    name: '',
    base_url: '',
    model: '',
    api_key: '',
    is_active: true
  }
}

// 格式化日期
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

// 页面初始化
onMounted(async () => {
  if (!checkAdminAccess()) return
  
  await fetchStats()
  await fetchApiConfigs()
})
</script>

<style scoped>
.admin-panel {
  min-height: 95vh;
  background: #f8fafc;
  padding: 2rem;
}

.admin-header {
  text-align: center;
  margin-bottom: 3rem;
}

.admin-header h1 {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.admin-header p {
  color: #64748b;
  font-size: 1.1rem;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-info h3 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.stat-info p {
  color: #64748b;
  margin: 0.25rem 0 0 0;
  font-size: 0.9rem;
}

/* 配置管理区域 */
.config-section {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

/* 系统设置 */
.settings-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.setting-item {
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.setting-item:hover {
  border-color: rgba(34, 197, 94, 0.3);
  background: rgba(34, 197, 94, 0.02);
}

.setting-info h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.setting-info p {
  color: #64748b;
  margin: 0;
  font-size: 0.9rem;
}

.limit-input-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.limit-input {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  text-align: center;
}

.limit-input:focus {
  outline: none;
  border-color: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

.limit-unit {
  color: #64748b;
  font-size: 0.9rem;
  font-weight: 500;
}

.update-btn {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.update-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
}

.update-btn:disabled {
  background: #d1d5db;
  color: #9ca3af;
  cursor: not-allowed;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.section-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(34, 197, 94, 0.3);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #64748b;
}

.empty-icon {
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1rem;
  color: #cbd5e1;
}

.empty-state h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  color: #475569;
}

/* 配置列表 */
.config-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.config-item {
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.config-item:hover {
  border-color: rgba(34, 197, 94, 0.3);
  background: rgba(34, 197, 94, 0.02);
}

.config-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.config-header h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.active {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-badge.inactive {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.config-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5rem;
}

.config-details p {
  margin: 0;
  font-size: 0.9rem;
  color: #64748b;
}

.config-details strong {
  color: #374151;
}

.config-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn {
  background: #f3f4f6;
  color: #374151;
}

.edit-btn:hover {
  background: #e5e7eb;
}

.delete-btn {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.2);
}

/* 弹窗样式 */
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
  backdrop-filter: blur(10px);
}

.modal {
  background: white;
  border-radius: 1rem;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
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

.modal-body {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.form-group input:focus {
  outline: none;
  border-color: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.1);
}

.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input {
  width: auto !important;
}

.modal-footer {
  padding: 1.5rem 2rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.cancel-btn, .submit-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: #f3f4f6;
  color: #374151;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.submit-btn {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(34, 197, 94, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-panel {
    padding: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .config-item {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }

  .setting-item {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .limit-input-group {
    justify-content: center;
  }

  .modal {
    width: 95%;
  }

  .modal-header, .modal-body, .modal-footer {
    padding: 1rem;
  }

  .modal-footer {
    flex-direction: column;
  }

  .cancel-btn, .submit-btn {
    width: 100%;
  }
}
</style>