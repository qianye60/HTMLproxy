<template>
  <div class="home-hero">
    <div class="container">
      <!-- 顶部标题区 -->
      <h1 class="main-title">灵枭HTML代理 - 极速网页发布新体验</h1>
      <h2 class="sub-title">一键托管 · 无需配置 · 绿色安全 · 全球可达</h2>
      <p class="desc">
        灵枭HTML代理为创作者、开发者和设计师提供极速、便捷的网页托管服务。无需服务器、无需域名，上传即刻生成全球可访问链接，让您的灵感瞬间上线，安全可靠，永久免费。
      </p>

      <!-- 特色功能区 -->
      <div class="features">
        <div class="feature" v-for="f in features" :key="f.title">
          <span class="feature-icon" v-html="f.svg"></span>
          <div class="feature-title">{{ f.title }}</div>
          <div class="feature-desc">{{ f.desc }}</div>
        </div>
      </div>

      <!-- 服务卡片区 -->
      <div class="cards">
        <div class="service-card" v-for="card in cards" :key="card.title">
          <span class="card-icon" v-html="card.svg"></span>
          <div class="card-title">{{ card.title }}</div>
          <div class="card-desc">{{ card.desc }}</div>
          <button 
            class="card-btn"
            :class="card.btnClass"
            @click="handleCardClick(card.title)"
          >
            {{ card.btn }}
          </button>
        </div>
      </div>

      <!-- 三步流程 -->
      <div class="steps-title">三步轻松发布您的网页</div>
      <div class="steps">
        <div class="step" v-for="(step, idx) in steps" :key="step.title">
          <div class="step-circle">{{ idx + 1 }}</div>
          <div class="step-title">{{ step.title }}</div>
          <div class="step-desc">{{ step.desc }}</div>
        </div>
      </div>

      <!-- 页脚 -->
      <footer class="footer">
        <div>
          <strong>灵枭HTML代理</strong> · 极速网页托管平台<br>
          <span class="footer-links">
            <a href="/about" @click.prevent>关于平台</a> |
            <a href="/contact" @click.prevent>联系我们</a> |
            <a href="/privacy" @click.prevent>隐私政策</a> |
            <a href="/terms" @click.prevent>服务条款</a>
          </span>
        </div>
        <div class="footer-copy">© 2025 灵枭HTML代理 保留所有权利</div>
      </footer>
    </div>

    <!-- 改进的弹窗组件 -->
    <Teleport to="body">
      <!-- 极速托管弹窗 -->
      <div v-if="showUploadModal" class="modal-overlay" @click="closeUploadModal">
        <div class="modal-content" @click.stop>
          <button class="modal-close" @click="closeUploadModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
          <div class="modal-header">
            <div class="modal-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect x="8" y="12" width="32" height="24" rx="6" stroke="#22c55e" stroke-width="3"/>
                <path d="M24 18v10M24 28l-4-4m4 4l4-4" stroke="#22c55e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h2>极速托管服务</h2>
          </div>
          <div class="modal-body">
            <p class="modal-description">
              体验最快速的HTML文件托管服务，让您的网页瞬间上线！
            </p>
            <div class="feature-list">
              <div class="feature-item">
                <span class="check-icon">✓</span>
                <span>拖拽上传，操作简单</span>
              </div>
              <div class="feature-item">
                <span class="check-icon">✓</span>
                <span>秒级生成访问链接</span>
              </div>
              <div class="feature-item">
                <span class="check-icon">✓</span>
                <span>支持HTML、CSS、JS等文件</span>
              </div>
              <div class="feature-item">
                <span class="check-icon">✓</span>
                <span>全球CDN加速访问</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="modal-btn secondary" @click="closeUploadModal">稍后再说</button>
            <button class="modal-btn primary" @click="goToControl">立即开始</button>
          </div>
        </div>
      </div>

      <!-- 多端兼容弹窗 -->
      <div v-if="showDetailsModal" class="modal-overlay" @click="closeDetailsModal">
        <div class="modal-content" @click.stop>
          <button class="modal-close" @click="closeDetailsModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
          <div class="modal-header">
            <div class="modal-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <circle cx="24" cy="24" r="20" stroke="#22c55e" stroke-width="3"/>
                <path d="M16 24h16M24 16v16" stroke="#22c55e" stroke-width="3" stroke-linecap="round"/>
              </svg>
            </div>
            <h2>多端完美兼容</h2>
          </div>
          <div class="modal-body">
            <p class="modal-description">
              您的网页将在所有设备上完美展示，无需额外配置
            </p>
            <div class="device-grid">
              <div class="device-item">
                <div class="device-icon">💻</div>
                <div class="device-name">桌面电脑</div>
                <div class="device-desc">完整功能体验</div>
              </div>
              <div class="device-item">
                <div class="device-icon">📱</div>
                <div class="device-name">智能手机</div>
                <div class="device-desc">触屏优化界面</div>
              </div>
              <div class="device-item">
                <div class="device-icon">📟</div>
                <div class="device-name">平板电脑</div>
                <div class="device-desc">自适应布局</div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="modal-btn primary full-width" @click="closeDetailsModal">我知道了</button>
          </div>
        </div>
      </div>

      <!-- 永久免费弹窗 -->
      <div v-if="showPolicyModal" class="modal-overlay" @click="closePolicyModal">
        <div class="modal-content" @click.stop>
          <button class="modal-close" @click="closePolicyModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
          <div class="modal-header">
            <div class="modal-icon">
              <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                <rect x="12" y="12" width="24" height="24" rx="6" stroke="#22c55e" stroke-width="3"/>
                <path d="M18 24h12" stroke="#22c55e" stroke-width="3" stroke-linecap="round"/>
              </svg>
            </div>
            <h2>永久免费承诺</h2>
          </div>
          <div class="modal-body">
            <p class="modal-description">
              我们承诺为所有用户提供永久免费的基础服务
            </p>
            <div class="policy-list">
              <div class="policy-item">
                <span class="policy-icon">🎯</span>
                <div class="policy-content">
                  <div class="policy-title">基础功能永久免费</div>
                  <div class="policy-desc">HTML托管、链接生成等核心功能</div>
                </div>
              </div>
              <div class="policy-item">
                <span class="policy-icon">🚫</span>
                <div class="policy-content">
                  <div class="policy-title">无隐藏费用</div>
                  <div class="policy-desc">透明收费，绝无额外隐藏费用</div>
                </div>
              </div>
              <div class="policy-item">
                <span class="policy-icon">♾️</span>
                <div class="policy-content">
                  <div class="policy-title">不限制网页数量</div>
                  <div class="policy-desc">可托管任意数量的网页项目</div>
                </div>
              </div>
              <div class="policy-item">
                <span class="policy-icon">🔄</span>
                <div class="policy-content">
                  <div class="policy-title">持续更新优化</div>
                  <div class="policy-desc">定期更新功能，优化用户体验</div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="modal-btn primary full-width" @click="closePolicyModal">太棒了！</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 响应式数据
const showUploadModal = ref(false)
const showDetailsModal = ref(false)
const showPolicyModal = ref(false)

// 静态数据
const features = [
  {
    svg: `<svg width="40" height="40" viewBox="0 0 40 40" fill="none"><circle cx="20" cy="20" r="18" stroke="#22c55e" stroke-width="3"/><polyline points="20,8 20,20 28,24" stroke="#22c55e" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    title: "秒速上线",
    desc: "上传即刻生成专属链接，网页立刻对外开放。"
  },
  {
    svg: `<svg width="40" height="40" viewBox="0 0 40 40" fill="none"><circle cx="20" cy="20" r="18" stroke="#22c55e" stroke-width="3"/><ellipse cx="20" cy="20" rx="10" ry="18" stroke="#22c55e" stroke-width="3" fill="none"/><line x1="2" y1="20" x2="38" y2="20" stroke="#22c55e" stroke-width="3"/></svg>`,
    title: "全球互通",
    desc: "无论身处何地，您的网页都能极速访问。"
  },
  {
    svg: `<svg width="40" height="40" viewBox="0 0 40 40" fill="none"><rect x="8" y="12" width="24" height="16" rx="4" stroke="#22c55e" stroke-width="3"/><path d="M12 20l6 6 10-10" stroke="#22c55e" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    title: "安全守护",
    desc: "数据加密存储，隐私与安全双重保障。"
  },
  {
    svg: `<svg width="40" height="40" viewBox="0 0 40 40" fill="none"><rect x="8" y="8" width="24" height="24" rx="6" stroke="#22c55e" stroke-width="3"/><path d="M16 20h8M20 16v8" stroke="#22c55e" stroke-width="3" stroke-linecap="round"/></svg>`,
    title: "零门槛操作",
    desc: "无需技术背景，界面友好，人人都能用。"
  }
]

const cards = [
  {
    svg: `<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><rect x="8" y="12" width="32" height="24" rx="6" stroke="#22c55e" stroke-width="3"/><path d="M24 18v10M24 28l-4-4m4 4l4-4" stroke="#22c55e" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    title: "极速托管",
    desc: "一键上传HTML文件，立即获得绿色专属访问通道。",
    btn: "立即体验",
    btnClass: "btn-green"
  },
  {
    svg: `<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><circle cx="24" cy="24" r="20" stroke="#22c55e" stroke-width="3"/><path d="M16 24h16M24 16v16" stroke="#22c55e" stroke-width="3" stroke-linecap="round"/></svg>`,
    title: "多端兼容",
    desc: "支持PC与移动端，自动适配各种屏幕，体验无缝切换。",
    btn: "了解详情",
    btnClass: "btn-outline"
  },
  {
    svg: `<svg width="48" height="48" viewBox="0 0 48 48" fill="none"><rect x="12" y="12" width="24" height="24" rx="6" stroke="#22c55e" stroke-width="3"/><path d="M18 24h12" stroke="#22c55e" stroke-width="3" stroke-linecap="round"/></svg>`,
    title: "永久免费",
    desc: "所有基础功能永久免费，无隐藏费用，放心使用。",
    btn: "查看政策",
    btnClass: "btn-outline"
  }
]

const steps = [
  { title: "上传文件", desc: "选择或拖拽HTML及相关资源，轻松上传。" },
  { title: "获取链接", desc: "系统自动生成绿色专属访问地址。" },
  { title: "一键分享", desc: "将链接分发给好友或社群，随时管理。" }
]

// 方法
const handleCardClick = (cardTitle) => {
  switch(cardTitle) {
    case '极速托管':
      showUploadModal.value = true
      break
    case '多端兼容':
      showDetailsModal.value = true
      break
    case '永久免费':
      showPolicyModal.value = true
      break
  }
}

const closeUploadModal = () => {
  showUploadModal.value = false
}

const closeDetailsModal = () => {
  showDetailsModal.value = false
}

const closePolicyModal = () => {
  showPolicyModal.value = false
}

const goToControl = () => {
  showUploadModal.value = false
  // 跳转到控制页面
  router.push('/control')
}

// 键盘事件处理
const handleKeydown = (event) => {
  if (event.key === 'Escape') {
    showUploadModal.value = false
    showDetailsModal.value = false
    showPolicyModal.value = false
  }
}

// 生命周期
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.home-hero {
  background: #f8fafc;
  min-height: 100vh;
  padding-top: 2.5rem;
  font-family: 'Inter', 'PingFang SC', 'Microsoft YaHei', Arial, sans-serif;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.main-title {
  font-size: 2.4rem;
  font-weight: 800;
  color: #1a3a2a;
  text-align: center;
  margin-bottom: 0.5rem;
  letter-spacing: 2px;
}

.sub-title {
  font-size: 1.3rem;
  color: #22c55e;
  text-align: center;
  margin-bottom: 1.2rem;
  font-weight: 600;
}

.desc {
  text-align: center;
  color: #4b5563;
  font-size: 1.1rem;
  margin-bottom: 2.2rem;
}

.features {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
}

.feature {
  flex: 1 1 180px;
  background: #fff;
  border-radius: 1rem;
  box-shadow: 0 2px 10px rgba(34,197,94,0.07);
  padding: 1.2rem 0.8rem;
  text-align: center;
  transition: box-shadow 0.2s, transform 0.2s;
}

.feature:hover {
  box-shadow: 0 8px 24px rgba(34,197,94,0.13);
  transform: translateY(-4px) scale(1.03);
}

.feature-icon {
  display: block;
  margin: 0 auto 0.5rem;
}

.feature-title {
  font-weight: 700;
  color: #22c55e;
  font-size: 1.1rem;
  margin-bottom: 0.2rem;
}

.feature-desc {
  color: #64748b;
  font-size: 0.98rem;
}

.cards {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
}

.service-card {
  flex: 1 1 260px;
  background: #fff;
  border-radius: 1.2rem;
  box-shadow: 0 2px 10px rgba(34,197,94,0.09);
  padding: 2rem 1.2rem 1.5rem 1.2rem;
  text-align: center;
  transition: box-shadow 0.2s, transform 0.2s;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.service-card:hover {
  box-shadow: 0 8px 24px rgba(34,197,94,0.15);
  transform: translateY(-4px) scale(1.03);
}

.card-icon {
  margin-bottom: 1rem;
}

.card-title {
  font-weight: 700;
  color: #1a3a2a;
  font-size: 1.15rem;
  margin-bottom: 0.5rem;
}

.card-desc {
  color: #64748b;
  font-size: 1rem;
  margin-bottom: 1.2rem;
}

.card-btn {
  padding: 0.5rem 1.5rem;
  border-radius: 2rem;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
}

.btn-green {
  background: #22c55e;
  color: #fff;
}

.btn-green:hover {
  background: #16a34a;
}

.btn-outline {
  background: #fff;
  color: #22c55e;
  border: 2px solid #22c55e;
}

.btn-outline:hover {
  background: #22c55e;
  color: #fff;
}

.steps-title {
  text-align: center;
  font-size: 1.2rem;
  color: #1a3a2a;
  font-weight: 700;
  margin-bottom: 1.2rem;
  margin-top: 2.5rem;
  letter-spacing: 1px;
}

.steps {
  display: flex;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
}

.step {
  flex: 1 1 180px;
  background: #f0fdf4;
  border-radius: 1rem;
  padding: 1.2rem 0.8rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(34,197,94,0.06);
}

.step-circle {
  width: 44px;
  height: 44px;
  background: #22c55e;
  color: #fff;
  border-radius: 50%;
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 0.6rem;
}

.step-title {
  font-weight: 700;
  color: #1a3a2a;
  font-size: 1.05rem;
  margin-bottom: 0.2rem;
}

.step-desc {
  color: #64748b;
  font-size: 0.97rem;
}

.footer {
  background: #22223b;
  color: #fff;
  border-radius: 1rem 1rem 0 0;
  margin-top: 3rem;
  padding: 2rem 0 1rem 0;
  text-align: center;
  font-size: 1rem;
}

.footer-links a {
  color: #22c55e;
  margin: 0 0.5rem;
  text-decoration: none;
  font-size: 0.98rem;
}

.footer-links a:hover {
  text-decoration: underline;
}

.footer-copy {
  color: #cbd5e1;
  font-size: 0.95rem;
  margin-top: 0.7rem;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  position: relative;
  background: white;
  border-radius: 1.5rem;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #f3f4f6;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
  z-index: 10;
}

.modal-close:hover {
  background: #e5e7eb;
  color: #374151;
}

.modal-header {
  text-align: center;
  padding: 2rem 2rem 1rem;
}

.modal-icon {
  margin-bottom: 1rem;
}

.modal-header h2 {
  color: #1f2937;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.modal-body {
  padding: 0 2rem 1rem;
}

.modal-description {
  color: #6b7280;
  font-size: 1rem;
  text-align: center;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
  background: #f9fafb;
  border-radius: 0.5rem;
}

.check-icon {
  width: 20px;
  height: 20px;
  background: #22c55e;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: bold;
  flex-shrink: 0;
}

.device-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.device-item {
  text-align: center;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.75rem;
}

.device-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.device-name {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.device-desc {
  font-size: 0.875rem;
  color: #6b7280;
}

.policy-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.policy-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: #f9fafb;
  border-radius: 0.75rem;
}

.policy-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.policy-content {
  flex: 1;
}

.policy-title {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.policy-desc {
  font-size: 0.875rem;
  color: #6b7280;
}

.modal-footer {
  padding: 1rem 2rem 2rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.modal-btn {
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  min-width: 100px;
}

.modal-btn.primary {
  background: #22c55e;
  color: white;
}

.modal-btn.primary:hover {
  background: #16a34a;
}

.modal-btn.secondary {
  background: #f3f4f6;
  color: #6b7280;
}

.modal-btn.secondary:hover {
  background: #e5e7eb;
  color: #374151;
}

.modal-btn.full-width {
  width: 100%;
}

@media (max-width: 900px) {
  .features, .cards, .steps {
    flex-direction: column;
    gap: 1.2rem;
  }
  
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
  
  .modal-header, .modal-body, .modal-footer {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  
  .device-grid {
    grid-template-columns: 1fr;
  }
}
</style>
