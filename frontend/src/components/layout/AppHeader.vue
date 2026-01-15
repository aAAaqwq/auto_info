<!-- AppHeader.vue - 顶部导航栏组件（架构版） -->
<template>
  <header class="app-header">
    <div class="container header-inner">
      <!-- Logo -->
      <router-link to="/" class="logo">
        <span class="logo-text">Auto Info</span>
      </router-link>

      <!-- 桌面导航 -->
      <nav class="nav-desktop">
        <router-link to="/" class="nav-item">首页</router-link>
        <router-link to="/articles" class="nav-item">文章库</router-link>
        <router-link v-for="cat in categories" :key="cat.slug" :to="`/category/${cat.slug}`" class="nav-item">
          {{ cat.name }}
        </router-link>
        <router-link to="/about" class="nav-item">关于</router-link>
      </nav>

      <!-- 右侧操作区 -->
      <div class="header-actions">
        <!-- 搜索按钮 -->
        <button class="search-btn" @click="openSearch">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
        </button>

        <!-- 移动端菜单按钮 -->
        <button class="menu-btn mobile-only" @click="toggleSidebar">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M3 12h18M3 6h18M3 18h18"/>
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
import { storeToRefs } from 'pinia'

const appStore = useAppStore()
const { categories } = storeToRefs(appStore)

const openSearch = () => {
  // TODO: 打开搜索弹窗
}

const toggleSidebar = () => {
  appStore.toggleSidebar()
}
</script>

<style lang="scss" scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: var(--bg-primary);
  border-bottom: 1px solid var(--border-light);
  z-index: 100;
}

.header-inner {
  height: 100%;
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.logo {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-color);
}

.nav-desktop {
  display: flex;
  gap: var(--spacing-md);
  flex: 1;
}

.nav-item {
  color: var(--text-secondary);
  font-size: 14px;
  padding: 4px 0;

  &.router-link-active {
    color: var(--primary-color);
  }
}

.header-actions {
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.search-btn, .menu-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: none;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);

  &:hover {
    background: var(--bg-secondary);
    color: var(--primary-color);
  }
}

.mobile-only {
  display: none;
}

@media (max-width: 768px) {
  .nav-desktop {
    display: none;
  }

  .mobile-only {
    display: flex;
  }
}
</style>
