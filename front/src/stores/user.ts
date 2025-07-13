import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

// 用户信息接口
interface UserInfo {
  username: string
  email: string
  avatar?: string
}

// 统计卡片接口
interface StatCard {
  id: string
  label: string
  value: string | number
  color: string
  iconColor: string
  icon: string
}

// 文件项接口
interface FileItem {
  id: number
  projectName: string
  editProjectName: string
  editing: boolean
  filename: string
  url: string
  size: string
  uploadTime: string
}

export const useUserStore = defineStore('user', () => {
  // 用户登录状态
  const isLoggedIn = ref(false)
  const token = ref('')
  
  // 用户信息
  const userInfo = reactive<UserInfo>({
    username: '',
    email: '',
    avatar: ''
  })
  
  // 统计数据
  const statCards = ref<StatCard[]>([
    {
      id: 'total-files',
      label: '文件总数',
      value: 0,
      color: '#dbeafe',
      iconColor: '#3b82f6',
      icon: 'FileIcon'
    },
    {
      id: 'remaining-space',
      label: '剩余空间',
      value: '50/50',
      color: '#dcfce7',
      iconColor: '#10b981',
      icon: 'StorageIcon'
    }
  ])
  
  // 文件列表
  const files = ref<FileItem[]>([])
  
  // 加载状态
  const isLoading = ref(false)
  const isUploading = ref(false)
  
  // 设置token
  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('JWTtoken', newToken)
  }
  
  // 清除token
  const clearToken = () => {
    token.value = ''
    localStorage.removeItem('JWTtoken')
  }
  
  // 检查登录状态
  const checkLoginStatus = async (): Promise<{ islogin: boolean; userauth?: boolean }> => {
    try {
      const storedToken = localStorage.getItem('JWTtoken')
      if (!storedToken) {
        isLoggedIn.value = false
        return { islogin: false }
      }
      
      // 设置token（如果还没有设置的话）
      if (token.value !== storedToken) {
        token.value = storedToken
      }
      
      const response = await axios.post('/verify', {}, {
        timeout: 5000,
        headers: {
          'Authorization': `Bearer ${storedToken}`
        }
      })
      
      if (response.data.islogin) {
        isLoggedIn.value = true
        token.value = storedToken
        return { islogin: true, userauth: response.data.userauth }
      } else {
        isLoggedIn.value = false
        clearToken()
        return { islogin: false }
      }
    } catch (error: any) {
      console.error('Token验证失败:', error)
      // 如果是网络错误或服务器错误，不清除token，保持当前状态
      if (error.code === 'NETWORK_ERROR' || error.response?.status >= 500) {
        return { islogin: false }
      }
      // 如果是401错误，说明token无效，清除token
      if (error.response?.status === 401) {
        isLoggedIn.value = false
        clearToken()
      }
      return { islogin: false }
    }
  }
  
  // 获取用户信息
  const fetchUserInfo = async () => {
    if (!token.value) return
    
    try {
      isLoading.value = true
      const response = await axios.get('/user/info', {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })
      
      Object.assign(userInfo, response.data)
    } catch (error) {
      console.error('获取用户信息失败:', error)
    } finally {
      isLoading.value = false
    }
  }
  
  // 获取统计数据
  const fetchStats = async () => {
    if (!token.value) return
    
    try {
      const response = await axios.get('/stats', {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })
      
      statCards.value = response.data
    } catch (error) {
      console.error('获取统计数据失败:', error)
    }
  }
  
  // 获取文件列表
  const fetchFiles = async () => {
    if (!token.value) return
    
    try {
      isLoading.value = true
      const response = await axios.get('/files', {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })
      
      files.value = response.data.map((file: any) => ({
        id: file.id,
        projectName: file.project_name,
        filename: file.filename,
        url: file.url, // 直接使用后端返回的相对路径，浏览器会基于当前页面域名解析
        size: file.size,
        uploadTime: file.upload_time,
        editProjectName: '',
        editing: false
      }))
      
      // 更新文件总数
      statCards.value[0].value = files.value.length
    } catch (error) {
      console.error('获取文件列表失败:', error)
    } finally {
      isLoading.value = false
    }
  }
  
  // 上传文件
  const uploadFile = async (file: File): Promise<FileItem | null> => {
    if (!token.value) return null
    
    try {
      isUploading.value = true
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await axios.post('/upload', formData, {
        headers: {
          'Authorization': `Bearer ${token.value}`,
          'Content-Type': 'multipart/form-data'
        }
      })
      
      const newFile = {
        id: response.data.id,
        projectName: response.data.project_name,
        filename: response.data.filename,
        url: response.data.url,
        size: response.data.size,
        uploadTime: response.data.upload_time,
        editProjectName: '',
        editing: false
      }
      
      files.value.unshift(newFile)
      statCards.value[0].value = files.value.length
      
      return newFile
    } catch (error) {
      console.error('上传文件失败:', error)
      throw error
    } finally {
      isUploading.value = false
    }
  }
  
  // 更新项目名
  const updateProjectName = async (fileId: number, projectName: string): Promise<boolean> => {
    if (!token.value) return false
    
    try {
      await axios.patch(`/files/${fileId}`, 
        { project_name: projectName },
        {
          headers: {
            'Authorization': `Bearer ${token.value}`
          }
        }
      )
      return true
    } catch (error) {
      console.error('更新项目名失败:', error)
      return false
    }
  }
  
  // 删除文件
  const deleteFile = async (fileId: number): Promise<boolean> => {
    if (!token.value) return false
    
    try {
      await axios.delete(`/files/${fileId}`, {
        headers: {
          'Authorization': `Bearer ${token.value}`
        }
      })
      
      files.value = files.value.filter(f => f.id !== fileId)
      statCards.value[0].value = files.value.length
      return true
    } catch (error) {
      console.error('删除文件失败:', error)
      return false
    }
  }
  
  // 初始化数据
  const initializeData = async () => {
    if (isLoggedIn.value && token.value) {
      await Promise.all([
        fetchUserInfo(),
        fetchStats(),
        fetchFiles()
      ])
    }
  }
  
  // 登出
  const logout = () => {
    isLoggedIn.value = false
    clearToken()
    userInfo.username = ''
    userInfo.email = ''
    userInfo.avatar = ''
    files.value = []
    statCards.value[0].value = 0
  }
  
  return {
    // 状态
    isLoggedIn,
    token,
    userInfo,
    statCards,
    files,
    isLoading,
    isUploading,
    
    // 方法
    setToken,
    clearToken,
    checkLoginStatus,
    fetchUserInfo,
    fetchStats,
    fetchFiles,
    uploadFile,
    updateProjectName,
    deleteFile,
    initializeData,
    logout
  }
}) 