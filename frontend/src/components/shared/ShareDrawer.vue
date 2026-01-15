<!-- ShareDrawer.vue - 分享抽屉组件 -->
<template>
  <teleport to="body">
    <!-- PC端右侧抽屉遮罩 -->
    <transition name="fade">
      <div v-if="show" class="drawer-overlay" @click="close"></div>
    </transition>

    <!-- PC端右侧抽屉 -->
    <transition name="slide-right">
      <div v-if="show" class="share-drawer pc-only">
        <div class="drawer-header">
          <h3>分享文章</h3>
          <button class="close-btn" @click="close">✕</button>
        </div>
        <div class="drawer-body">
          <!-- 一键原生分享（移动端首选） -->
          <button class="one-click-share" @click="nativeShare">
            <span class="one-click-icon">⚡</span>
            <span class="one-click-text">一键分享</span>
            <span class="one-click-hint">调起系统分享菜单</span>
          </button>

          <div class="section-title">其他方式</div>

          <div class="share-platforms">
            <button class="platform-btn" @click="copyWithTitle">
              <span class="platform-icon">📋</span>
              <span class="platform-name">复制标题+链接</span>
            </button>
            <button class="platform-btn" @click="showWechatQR = true">
              <span class="platform-icon">💬</span>
              <span class="platform-name">微信扫码</span>
            </button>
            <button class="platform-btn" @click="shareToWeibo">
              <span class="platform-icon">📱</span>
              <span class="platform-name">微博</span>
            </button>
            <button class="platform-btn" @click="shareToXiaohongshu">
              <span class="platform-icon">📕</span>
              <span class="platform-name">小红书</span>
            </button>
          </div>

          <!-- 微信二维码 -->
          <transition name="fade">
            <div v-if="showWechatQR" class="wechat-qr">
              <p class="qr-tip">扫码分享到微信</p>
              <div class="qr-code" ref="qrCodeRef">
                <img v-if="qrCodeUrl" :src="qrCodeUrl" alt="微信二维码" />
                <div v-else class="qr-loading">生成中...</div>
              </div>
              <button class="qr-close" @click="showWechatQR = false">关闭</button>
            </div>
          </transition>
        </div>
      </div>
    </transition>

    <!-- 移动端底部弹出 -->
    <transition name="slide-up">
      <div v-if="show" class="share-sheet mobile-only">
        <div class="sheet-header">
          <span class="sheet-cancel" @click="close">取消</span>
          <span class="sheet-title">分享文章</span>
          <span class="sheet-placeholder"></span>
        </div>
        <div class="sheet-body">
          <button class="sheet-btn primary" @click="nativeShare">
            <span class="sheet-icon">⚡</span>
            <span class="sheet-name">一键分享</span>
          </button>
          <button class="sheet-btn" @click="copyWithTitle">
            <span class="sheet-icon">📋</span>
            <span class="sheet-name">复制标题+链接</span>
          </button>
          <button class="sheet-btn" @click="showWechatQR = true">
            <span class="sheet-icon">💬</span>
            <span class="sheet-name">微信扫码</span>
          </button>
          <button class="sheet-btn" @click="shareToWeibo">
            <span class="sheet-icon">📱</span>
            <span class="sheet-name">微博</span>
          </button>
          <button class="sheet-btn" @click="shareToXiaohongshu">
            <span class="sheet-icon">📕</span>
            <span class="sheet-name">小红书</span>
          </button>
        </div>

        <!-- 微信二维码 -->
        <transition name="fade">
          <div v-if="showWechatQR" class="wechat-modal">
            <div class="modal-content">
              <p class="qr-tip">扫码分享到微信</p>
              <div class="qr-code">
                <img v-if="qrCodeUrl" :src="qrCodeUrl" alt="微信二维码" />
                <div v-else class="qr-loading">生成中...</div>
              </div>
              <button class="modal-close" @click="showWechatQR = false">关闭</button>
            </div>
          </div>
        </transition>
      </div>
    </transition>

    <!-- Toast提示 -->
    <transition name="fade">
      <div v-if="toast" class="toast">{{ toast }}</div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: ''
  },
  url: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close'])

const showWechatQR = ref(false)
const qrCodeUrl = ref('')
const toast = ref('')

const close = () => {
  emit('close')
}

const showToast = (msg) => {
  toast.value = msg
  setTimeout(() => {
    toast.value = ''
  }, 2000)
}

// 复制链接
const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(props.url)
    showToast('链接已复制到剪贴板')
  } catch (e) {
    const input = document.createElement('input')
    input.value = props.url
    document.body.appendChild(input)
    input.select()
    document.execCommand('copy')
    document.body.removeChild(input)
    showToast('链接已复制')
  }
}

// 分享到微博
const shareToWeibo = () => {
  const shareUrl = 'https://service.weibo.com/share/share.php?url=' + encodeURIComponent(props.url) + '&title=' + encodeURIComponent(props.title)
  window.open(shareUrl, '_blank')
}

// 分享到小红书
const shareToXiaohongshu = () => {
  copyLink()
  showToast('已复制，请在小红书App内粘贴')
}

// 一键原生分享
const nativeShare = async () => {
  if (navigator.share) {
    try {
      await navigator.share({
        title: props.title,
        text: props.title,
        url: props.url
      })
      showToast('分享成功')
      close()
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error('Share failed:', err)
      }
    }
  } else {
    copyLink()
  }
}

// 复制文章标题+链接
const copyWithTitle = async () => {
  const text = props.title + '\n' + props.url
  try {
    await navigator.clipboard.writeText(text)
    showToast('标题和链接已复制')
  } catch (e) {
    copyLink()
  }
}

// 生成微信二维码
const generateQRCode = () => {
  if (!props.url) return
  qrCodeUrl.value = 'https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=' + encodeURIComponent(props.url)
}

watch(showWechatQR, (show) => {
  if (show) {
    generateQRCode()
  }
})
</script>

<style lang="scss" scoped>
.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.share-drawer {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 400px;
  background: var(--bg-primary);
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  z-index: 1001;
  display: flex;
  flex-direction: column;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid var(--border-light);

  h3 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
  }
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  font-size: 20px;
  cursor: pointer;
  color: var(--text-secondary);
  border-radius: 50%;

  &:hover {
    background: var(--bg-tertiary);
  }
}

.one-click-share {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  margin-bottom: 20px;
  transition: transform 0.2s, box-shadow 0.2s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  &:active {
    transform: translateY(0);
  }
}

.one-click-icon {
  font-size: 24px;
}

.one-click-text {
  flex: 1;
  text-align: left;
  font-size: 16px;
  font-weight: 600;
}

.one-click-hint {
  font-size: 12px;
  opacity: 0.8;
}

.section-title {
  font-size: 13px;
  color: var(--text-tertiary);
  margin: 0 0 12px 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.drawer-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.share-platforms {
  display: grid;
  gap: 12px;
}

.platform-btn {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  background: transparent;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    background: var(--bg-secondary);
    border-color: var(--primary-color);
  }
}

.platform-icon {
  font-size: 24px;
}

.platform-name {
  font-size: 16px;
  color: var(--text-primary);
}

.wechat-qr {
  margin-top: 20px;
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  text-align: center;
}

.qr-tip {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: var(--text-secondary);
}

.qr-code {
  width: 200px;
  height: 200px;
  margin: 0 auto 16px;
  background: #fff;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;

  img {
    width: 100%;
    height: 100%;
    border-radius: var(--radius-sm);
  }
}

.qr-loading {
  color: var(--text-tertiary);
}

.qr-close {
  padding: 8px 24px;
  border: none;
  background: var(--primary-color);
  color: white;
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.share-sheet {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--bg-primary);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1001;
}

.sheet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--border-light);
}

.sheet-cancel {
  font-size: 16px;
  color: var(--primary-color);
  cursor: pointer;
}

.sheet-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-primary);
}

.sheet-placeholder {
  width: 40px;
}

.sheet-body {
  display: flex;
  padding: 20px;
  gap: 20px;
  overflow-x: auto;
}

.sheet-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 70px;
  border: none;
  background: transparent;
  cursor: pointer;

  &.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: var(--radius-md);
    padding: 12px;

    .sheet-icon {
      font-size: 32px;
    }

    .sheet-name {
      color: white;
      font-weight: 600;
    }
  }
}

.sheet-icon {
  font-size: 28px;
}

.sheet-name {
  font-size: 12px;
  color: var(--text-secondary);
}

.wechat-modal {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: var(--bg-primary);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

.modal-content {
  padding: 20px;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  text-align: center;
}

.modal-close {
  margin-top: 16px;
  padding: 8px 24px;
  border: none;
  background: var(--primary-color);
  color: white;
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.toast {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 12px 24px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  border-radius: var(--radius-md);
  z-index: 2000;
  font-size: 14px;
}

.pc-only {
  @media (max-width: 768px) {
    display: none;
  }
}

.mobile-only {
  display: none;

  @media (max-width: 768px) {
    display: block;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-right-enter-active,
.slide-right-leave-active {
  transition: transform 0.3s;
}

.slide-right-enter-from,
.slide-right-leave-to {
  transform: translateX(100%);
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: transform 0.3s;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100%);
}
</style>
