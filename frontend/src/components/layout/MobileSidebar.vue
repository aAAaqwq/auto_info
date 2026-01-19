<!-- MobileSidebar.vue - 移动端侧边栏组件 -->
<template>
  <!-- 遮罩层 -->
  <Transition name="fade">
    <div v-if="isOpen" class="sidebar-overlay" @click="close"></div>
  </Transition>

  <!-- 侧边栏 -->
  <Transition name="slide">
    <div v-if="isOpen" class="mobile-sidebar">
      <!-- 头部 -->
      <div class="sidebar-header">
        <router-link to="/" class="logo" @click="close">
          <span class="logo-icon">&lt;/&gt;</span>
          <span class="logo-text gradient-text">Auto Info</span>
        </router-link>
        <button class="close-btn" @click="close">
          <span class="close-icon">×</span>
        </button>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" @click="close">
          <span class="nav-icon">⌂</span>
          <span class="nav-text">首页</span>
        </router-link>
        <router-link to="/articles" class="nav-item" @click="close">
          <span class="nav-icon">◈</span>
          <span class="nav-text">文章库</span>
        </router-link>

        <!-- 分类菜单 -->
        <div v-if="categories.length > 0" class="nav-section">
          <div class="nav-section-title">分类</div>
          <router-link
            v-for="cat in categories"
            :key="cat.slug"
            :to="`/category/${cat.slug}`"
            class="nav-item nav-item-sub"
            @click="close"
          >
            <span class="nav-icon">◇</span>
            <span class="nav-text">{{ cat.name }}</span>
          </router-link>
        </div>

        <router-link to="/about" class="nav-item" @click="close">
          <span class="nav-icon">⍰</span>
          <span class="nav-text">关于</span>
        </router-link>
      </nav>

      <!-- 底部操作区 -->
      <div class="sidebar-footer">
        <button class="theme-toggle-btn" @click="toggleTheme">
          <span class="theme-icon">{{ isDark ? '☀️' : '🌙' }}</span>
          <span class="theme-text">{{ isDark ? '切换到亮色模式' : '切换到暗色模式' }}</span>
        </button>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed } from 'vue'
import { useAppStore } from '@/stores/app'
import { storeToRefs } from 'pinia'

const appStore = useAppStore()
const { categories, sidebarOpen, isDark } = storeToRefs(appStore)

const isOpen = computed(() => sidebarOpen.value)

const close = () => {
  appStore.closeSidebar()
}

const toggleTheme = () => {
  appStore.toggleTheme()
}
</script>

<style lang="scss" scoped>
// 遮罩层
.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 998;
}

// 侧边栏
.mobile-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 280px;
  max-width: 80vw;
  background: var(--bg-primary);
  border-right: 1px solid var(--border-color);
  z-index: 999;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-lg);
}

// 头部
.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border-bottom: 1px solid var(--border-color);

  .logo {
    display: flex;
    align-items: center;
    gap: 8px;
    text-decoration: none;
  }

  .logo-icon {
    font-size: 20px;
    color: var(--accent-cyan);
  }

  .logo-text {
    font-size: 20px;
    font-weight: 700;
  }
}

.close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: all 0.2s;

  &:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
  }
}

.close-icon {
  font-size: 28px;
  line-height: 1;
}

// 导航
.sidebar-nav {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
}

.nav-section {
  margin-top: 16px;
}

.nav-section-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 1px;
  padding: 8px 12px;
  margin-bottom: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: var(--radius-sm);
  transition: all 0.2s;
  font-size: 15px;

  &:hover {
    background: var(--bg-secondary);
    color: var(--text-primary);
  }

  &.router-link-active {
    background: var(--bg-secondary);
    color: var(--accent-cyan);
    font-weight: 500;
  }
}

.nav-item-sub {
  padding-left: 24px;
  font-size: 14px;
}

.nav-icon {
  font-size: 16px;
  opacity: 0.7;
  width: 20px;
  text-align: center;
}

.router-link-active .nav-icon {
  opacity: 1;
}

// 底部
.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border-color);
}

.theme-toggle-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: transparent;
  color: var(--text-primary);
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    border-color: var(--primary-color);
    background: var(--bg-secondary);
  }
}

.theme-icon {
  font-size: 18px;
}

// 动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease-out;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}
</style>
