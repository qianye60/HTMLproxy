<template>
  <div class="html-proxy-hero">
    <!-- 动态背景网格 -->
    <div class="bg-grid"></div>
    
    <!-- 主要内容区域 -->
    <div class="hero-container">
      <!-- 英雄区域 -->
      <section class="hero-section">
        <div class="hero-badge">
          <Zap class="badge-icon" />
          <span>HTML 极速托管</span>
        </div>
        
        <h1 class="hero-title">
          <span class="main-text">将您的 HTML</span>
          <br />
          <span class="highlight-text">瞬间发布全球</span>
        </h1>
        
        <p class="hero-subtitle">
          专业的 HTML 文件托管服务，无需服务器、无需域名配置
          <br>
          <strong>3秒上线 • 全球访问 • 永久免费 • 极速稳定</strong>
        </p>

        <div class="hero-actions">
          <button class="primary-btn" @click="quickStart">
            <Upload class="btn-icon" />
            立即上传文件
          </button>
          <button class="secondary-btn" @click="tryAIGenerator">
            <Sparkles class="btn-icon" />
            AI生成网站
          </button>
          <button class="tertiary-btn" @click="viewDemo">
            <Eye class="btn-icon" />
            查看演示
          </button>
        </div>

        <!-- 实时统计 -->
        <div class="stats-bar">
          <div class="stat-item">
            <Globe class="stat-icon" />
            <span class="stat-number">50,000+</span>
            <span class="stat-label">文件已托管</span>
          </div>
          <div class="stat-item">
            <Clock class="stat-icon" />
            <span class="stat-number">< 3秒</span>
            <span class="stat-label">上线速度</span>
          </div>
          <div class="stat-item">
            <Shield class="stat-icon" />
            <span class="stat-number">99.9%</span>
            <span class="stat-label">稳定运行</span>
          </div>
        </div>
      </section>

      <!-- 核心优势区域 -->
      <section class="features-section">
        <div class="section-header">
          <h2 class="section-title">为什么选择灵枭HTML代理？</h2>
          <p class="section-subtitle">专业、快速、可靠的HTML文件托管解决方案</p>
        </div>

        <div class="features-grid">
          <div class="feature-card" v-for="feature in features" :key="feature.id">
            <div class="feature-icon">
              <component :is="feature.icon" />
            </div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-desc">{{ feature.description }}</p>
            <div class="feature-highlight">{{ feature.highlight }}</div>
          </div>
        </div>
      </section>

      <!-- 使用流程 -->
      <section class="workflow-section">
        <div class="section-header">
          <h2 class="section-title">三步完成全球发布</h2>
          <p class="section-subtitle">简单到不可思议的发布流程</p>
        </div>

        <div class="workflow-steps">
          <div class="step-item" v-for="(step, index) in workflowSteps" :key="index">
            <div class="step-number">{{ index + 1 }}</div>
            <div class="step-content">
              <div class="step-icon">
                <component :is="step.icon" />
              </div>
              <h3 class="step-title">{{ step.title }}</h3>
              <p class="step-desc">{{ step.description }}</p>
            </div>
            <div v-if="index < workflowSteps.length - 1" class="step-connector">
              <ArrowRight class="connector-icon" />
            </div>
          </div>
        </div>
      </section>

      <!-- 技术特性 -->
      <section class="tech-section">
        <div class="tech-grid">
          <div class="tech-card">
            <div class="tech-header">
              <Server class="tech-icon" />
              <h3>无需服务器</h3>
            </div>
            <p>告别复杂的服务器配置和维护，我们的云基础设施为您处理一切技术细节</p>
            <div class="tech-tags">
              <span class="tag">零配置</span>
              <span class="tag">自动扩展</span>
              <span class="tag">高可用</span>
            </div>
          </div>

          <div class="tech-card">
            <div class="tech-header">
              <Globe class="tech-icon" />
              <h3>全球CDN加速</h3>
            </div>
            <p>基于全球CDN网络分发，确保您的HTML页面在世界任何角落都能极速加载</p>
            <div class="tech-tags">
              <span class="tag">全球节点</span>
              <span class="tag">智能路由</span>
              <span class="tag">极速访问</span>
            </div>
          </div>

          <div class="tech-card">
            <div class="tech-header">
              <Shield class="tech-icon" />
              <h3>安全可靠</h3>
            </div>
            <p>企业级安全防护，SSL加密传输，确保您的文件和访问者数据绝对安全</p>
            <div class="tech-tags">
              <span class="tag">SSL加密</span>
              <span class="tag">DDoS防护</span>
              <span class="tag">数据备份</span>
            </div>
          </div>
        </div>
      </section>

      <!-- 支持的文件类型 -->
      <section class="file-types-section">
        <div class="section-header">
          <h2 class="section-title">支持多种文件格式</h2>
          <p class="section-subtitle">完整的前端项目托管支持</p>
        </div>

        <div class="file-types-grid">
          <div class="file-type-item" v-for="fileType in fileTypes" :key="fileType.name">
            <div class="file-icon" :style="{ backgroundColor: fileType.color }">
              <component :is="fileType.icon" />
            </div>
            <h4>{{ fileType.name }}</h4>
            <p>{{ fileType.description }}</p>
          </div>
        </div>
      </section>

      <!-- 行动召唤 -->
      <section class="cta-section">
        <div class="cta-content">
          <div class="cta-icon">
            <Rocket />
          </div>
          <h2 class="cta-title">准备发布您的HTML项目？</h2>
          <p class="cta-subtitle">
            立即体验最快速的HTML文件托管服务，让您的作品瞬间上线
          </p>
          <button class="cta-button" @click="getStarted">
            <Upload class="btn-icon" />
            免费开始使用
            <ArrowRight class="btn-arrow" />
          </button>
          <p class="cta-note">无需注册 • 完全免费 • 即刻开始</p>
        </div>
      </section>
    </div>

    <!-- 快速演示弹窗 -->
    <div v-if="showDemoModal" class="modal-overlay" @click="closeDemoModal">
      <div class="demo-modal" @click.stop>
        <div class="modal-header">
          <div class="demo-avatar">
            <Play class="avatar-icon" />
          </div>
          <h3>快速演示</h3>
          <button class="close-btn" @click="closeDemoModal">
            <X />
          </button>
        </div>
        <div class="modal-body">
          <div class="demo-steps">
            <div class="demo-step">
              <div class="step-number">1</div>
              <div class="step-content">
                <h4>选择HTML文件</h4>
                <p>点击上传按钮，选择您的HTML文件及相关资源</p>
              </div>
            </div>
            <div class="demo-step">
              <div class="step-number">2</div>
              <div class="step-content">
                <h4>自动处理</h4>
                <p>系统自动上传并配置您的文件到全球CDN网络</p>
              </div>
            </div>
            <div class="demo-step">
              <div class="step-number">3</div>
              <div class="step-content">
                <h4>获得链接</h4>
                <p>立即获得永久访问链接，可以分享给任何人</p>
              </div>
            </div>
          </div>
          <div class="demo-example">
            <div class="example-url">
              <Globe class="url-icon" />
              <span>https://html.lingxiao.com/your-project</span>
              <button class="copy-btn">
                <Copy />
              </button>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="demo-start-btn" @click="startDemo">
            立即体验
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Zap, Upload, Eye, Globe, Clock, Shield, Server, Rocket, 
  ArrowRight, Play, X, Copy, FileText, Image, Code, Palette, Sparkles
} from 'lucide-vue-next'

const router = useRouter()
const showDemoModal = ref(false)

// 核心功能数据
const features = ref([
  {
    id: 1,
    icon: Zap,
    title: '极速上线',
    description: '上传文件后3秒内即可生成全球访问链接，无需等待任何配置过程',
    highlight: '3秒极速部署'
  },
  {
    id: 2,
    icon: Globe,
    title: '全球访问',
    description: '基于全球CDN网络，确保您的HTML页面在世界任何地方都能快速加载',
    highlight: '全球CDN加速'
  },
  {
    id: 3,
    icon: Server,
    title: '无需服务器',
    description: '告别复杂的服务器购买、配置和维护，专注于您的内容创作',
    highlight: '零运维成本'
  },
  {
    id: 4,
    icon: Shield,
    title: '安全稳定',
    description: 'SSL加密传输，企业级安全防护，99.9%稳定运行保障',
    highlight: '企业级安全'
  },
  {
    id: 5,
    icon: Upload,
    title: '简单易用',
    description: '拖拽上传，一键发布，无需任何技术背景即可轻松使用',
    highlight: '零技术门槛'
  },
  {
    id: 6,
    icon: Clock,
    title: '永久免费',
    description: '核心功能永久免费，无隐藏费用，让您的创意不受限制',
    highlight: '完全免费'
  }
])

// 工作流程步骤
const workflowSteps = ref([
  {
    icon: Upload,
    title: '上传HTML文件',
    description: '选择您的HTML文件及相关资源，支持拖拽上传'
  },
  {
    icon: Zap,
    title: '自动部署',
    description: '系统自动处理并部署到全球CDN网络'
  },
  {
    icon: Globe,
    title: '获得链接',
    description: '立即获得永久访问链接，可随时分享'
  }
])

// 支持的文件类型
const fileTypes = ref([
  {
    name: 'HTML',
    description: '网页主文件',
    icon: FileText,
    color: '#22c55e'
  },
  {
    name: 'CSS',
    description: '样式文件',
    icon: Palette,
    color: '#3b82f6'
  },
  {
    name: 'JavaScript',
    description: '脚本文件',
    icon: Code,
    color: '#f59e0b'
  }
])

// 方法
const quickStart = () => {
  router.push('/control')
}

const tryAIGenerator = () => {
  router.push('/ai-generator')
}

const viewDemo = () => {
  showDemoModal.value = true
}

const closeDemoModal = () => {
  showDemoModal.value = false
}

const startDemo = () => {
  showDemoModal.value = false
  router.push('/control')
}

const getStarted = () => {
  router.push('/control')
}

// 动画效果
onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in')
      }
    })
  })

  document.querySelectorAll('.feature-card, .step-item, .tech-card, .file-type-item').forEach(el => {
    observer.observe(el)
  })
})
</script>

<style scoped>
/* 全局样式 */
.html-proxy-hero {
  min-height: 95vh;
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
  color: #1e293b;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  position: relative;
  overflow-x: hidden;
}

/* 背景网格 */
.bg-grid {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(34, 197, 94, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(34, 197, 94, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  pointer-events: none;
  z-index: 0;
}

/* 主容器 */
.hero-container {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* 英雄区域 */
.hero-section {
  text-align: center;
  padding: 6rem 0 4rem;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: #22c55e;
  margin-bottom: 2rem;
}

.badge-icon {
  width: 1rem;
  height: 1rem;
}

.hero-title {
  font-size: clamp(3rem, 8vw, 5rem);
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  letter-spacing: -0.02em;
}

.main-text {
  color: #1e293b;
}

.highlight-text {
  color: #22c55e;
  position: relative;
}

.highlight-text::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #22c55e, #16a34a);
  border-radius: 2px;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  color: #64748b;
  max-width: 800px;
  margin: 0 auto 3rem;
}

.hero-subtitle strong {
  color: #22c55e;
  font-weight: 700;
}

/* 按钮样式 */
.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 4rem;
  flex-wrap: wrap;
}

.primary-btn, .secondary-btn, .tertiary-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 1.1rem;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
}

.primary-btn {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  box-shadow: 0 10px 25px rgba(34, 197, 94, 0.3);
}

.primary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(34, 197, 94, 0.4);
}

.secondary-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
}

.secondary-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 15px 35px rgba(59, 130, 246, 0.4);
}

.tertiary-btn {
  background: white;
  color: #22c55e;
  border: 2px solid #22c55e;
}

.tertiary-btn:hover {
  background: #22c55e;
  color: white;
  transform: translateY(-2px);
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* 统计栏 */
.stats-bar {
  display: flex;
  justify-content: center;
  gap: 3rem;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.stat-icon {
  width: 2rem;
  height: 2rem;
  color: #22c55e;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-label {
  font-size: 0.9rem;
  color: #64748b;
}

/* 功能区域 */
.features-section {
  padding: 4rem 0;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #1e293b;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #64748b;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 2rem;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.feature-card.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.feature-card:hover {
  transform: translateY(-5px);
  border-color: rgba(34, 197, 94, 0.3);
  box-shadow: 0 20px 40px rgba(34, 197, 94, 0.1);
}

.feature-icon {
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
  color: white;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #1e293b;
}

.feature-desc {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.feature-highlight {
  display: inline-block;
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.9rem;
  font-weight: 600;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

/* 工作流程 */
.workflow-section {
  padding: 4rem 0;
  background: white;
  margin: 2rem 0;
  border-radius: 2rem;
}

.workflow-steps {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.step-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  opacity: 0;
  transform: translateX(-20px);
  transition: all 0.5s ease;
}

.step-item.animate-in {
  opacity: 1;
  transform: translateX(0);
}

.step-number {
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  color: white;
  flex-shrink: 0;
}

.step-content {
  text-align: center;
  max-width: 200px;
}

.step-icon {
  width: 2rem;
  height: 2rem;
  color: #22c55e;
  margin: 0 auto 1rem;
}

.step-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1e293b;
}

.step-desc {
  color: #64748b;
  font-size: 0.9rem;
  line-height: 1.4;
}

.step-connector {
  color: #22c55e;
}

.connector-icon {
  width: 1.5rem;
  height: 1.5rem;
}

/* 技术优势 */
.tech-section {
  padding: 4rem 0;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.tech-card {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 2rem;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.tech-card.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.tech-card:hover {
  border-color: rgba(34, 197, 94, 0.3);
  transform: translateY(-3px);
  box-shadow: 0 15px 30px rgba(34, 197, 94, 0.1);
}

.tech-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.tech-icon {
  width: 2rem;
  height: 2rem;
  color: #22c55e;
}

.tech-header h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #1e293b;
}

.tech-card p {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.tech-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.tag {
  background: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

/* 文件类型支持 */
.file-types-section {
  padding: 4rem 0;
  background: white;
  margin: 2rem 0;
  border-radius: 2rem;
}

.file-types-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
}

.file-type-item {
  text-align: center;
  padding: 2rem 1rem;
  border-radius: 1rem;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
}

.file-type-item.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.file-type-item:hover {
  transform: translateY(-5px);
}

.file-icon {
  width: 4rem;
  height: 4rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  color: white;
}

.file-type-item h4 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #1e293b;
}

.file-type-item p {
  color: #64748b;
  font-size: 0.9rem;
}

/* 行动召唤 */
.cta-section {
  padding: 6rem 0;
  text-align: center;
}

.cta-content {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 2rem;
  padding: 4rem 2rem;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0 10px 25px rgba(34, 197, 94, 0.1);
}

.cta-icon {
  width: 4rem;
  height: 4rem;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2rem;
  color: white;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #1e293b;
}

.cta-subtitle {
  font-size: 1.2rem;
  color: #64748b;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  border: none;
  padding: 1.25rem 2.5rem;
  border-radius: 1rem;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 15px 35px rgba(34, 197, 94, 0.3);
}

.cta-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 20px 45px rgba(34, 197, 94, 0.4);
}

.btn-arrow {
  width: 1.25rem;
  height: 1.25rem;
  transition: transform 0.3s ease;
}

.cta-button:hover .btn-arrow {
  transform: translateX(3px);
}

.cta-note {
  margin-top: 1.5rem;
  color: #64748b;
  font-size: 0.9rem;
}

/* 演示弹窗 */
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

.demo-modal {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 1.5rem;
  max-width: 500px;
  width: 90%;
  overflow: hidden;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  border-bottom: 1px solid #e2e8f0;
  position: relative;
}

.demo-avatar {
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.avatar-icon {
  width: 1.5rem;
  height: 1.5rem;
}

.modal-header h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
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

.demo-steps {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.demo-step {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.demo-step .step-number {
  width: 2rem;
  height: 2rem;
  background: #22c55e;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
  flex-shrink: 0;
}

.demo-step .step-content h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.demo-step .step-content p {
  color: #64748b;
  margin: 0;
  line-height: 1.5;
}

.demo-example {
  background: #f8fafc;
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
}

.example-url {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: white;
  padding: 1rem;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
}

.url-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #22c55e;
  flex-shrink: 0;
}

.example-url span {
  flex: 1;
  font-family: 'Fira Code', monospace;
  font-size: 0.9rem;
  color: #1e293b;
}

.copy-btn {
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: all 0.2s ease;
}

.copy-btn:hover {
  background: #f1f5f9;
  color: #22c55e;
}

.modal-footer {
  padding: 2rem;
  border-top: 1px solid #e2e8f0;
}

.demo-start-btn {
  width: 100%;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.demo-start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(34, 197, 94, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-container {
    padding: 0 1rem;
  }
  
  .hero-section {
    padding: 3.5rem 0 2.5rem;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .primary-btn, .secondary-btn, .tertiary-btn {
    width: 100%;
    max-width: 300px;
    justify-content: center;
  }
  
  .stats-bar {
    gap: 2rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .workflow-steps {
    flex-direction: column;
    gap: 3rem;
  }
  
  .step-connector {
    transform: rotate(90deg);
  }
  
  .tech-grid {
    grid-template-columns: 1fr;
  }
  
  .file-types-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .cta-content {
    padding: 2.5rem 1.2rem;
  }
  
  .cta-title {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .feature-card {
    padding: 1.5rem;
  }
  
  .file-types-grid {
    grid-template-columns: 1fr;
  }
}
</style>