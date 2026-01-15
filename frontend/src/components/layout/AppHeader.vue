<!-- AppHeader.vue - 顶部导航栏组件（极客风） -->
<template>
  <header class="app-header">
    <div class="container header-inner">
      <router-link to="/" class="logo">
        <span class="logo-icon">&lt;/&gt;</span>
        <span class="logo-text gradient-text">Auto Info</span>
      </router-link>

      <nav class="nav-desktop">
        <router-link to="/" class="nav-item">
          <span class="nav-icon">⌂</span>
          <span class="nav-text">首页</span>
        </router-link>
        <router-link to="/articles" class="nav-item">
          <span class="nav-icon">◈</span>
          <span class="nav-text">文章库</span>
        </router-link>
        <router-link v-for="cat in categories" :key="cat.slug" :to="`/category/${cat.slug}`" class="nav-item">
          <span class="nav-icon">◇</span>
          <span class="nav-text">{{ cat.name }}</span>
        </router-link>
        <router-link to="/about" class="nav-item">
          <span class="nav-icon">⍰</span>
          <span class="nav-text">关于</span>
        </router-link>
      </nav>

      <div class="header-actions">
        <InstantSearch />
        <button class="menu-btn mobile-only" @click="toggleSidebar">
          <span class="hamburger"></span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
import { storeToRefs } from 'pinia'
import InstantSearch from '@/components/shared/InstantSearch.vue'

const appStore = useAppStore()
const { categories } = storeToRefs(appStore)

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
  height: 70px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
  z-index: 100;

  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--primary-color), var(--accent-purple), transparent);
  }
}

.header-inner {
  height: 100%;
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  padding: 8px 16px;
  border-radius: 12px;
  transition: all 0.3s;

  &:hover {
    background: var(--bg-secondary);
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.4);
  }
}

.logo-icon {
  font-size: 18px;
  color: var(--accent-cyan);
  text-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
}

.logo-text {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.nav-desktop {
  display: flex;
  gap: 4px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: var(--text-secondary);
  font-size: 14px;
  padding: 10px 16px;
  border-radius: 6px;
  text-decoration: none;
  transition: all 0.3s;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
    transition: all 0.3s;
    transform: translateX(-50%);
  }

  &:hover {
    color: var(--primary-color);
    background: var(--bg-secondary);

    &::before {
      width: 80%;
    }
  }

  &.router-link-active {
    color: var(--accent-cyan);

    &::before {
      width: 80%;
      box-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
    }
  }
}

.nav-icon {
  font-size: 12px;
  opacity: 0.6;
  transition: opacity 0.15s;
}

.nav-item:hover .nav-icon {
  opacity: 1;
}

.header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.menu-btn {
  width: 44px;
  height: 44px;
  border-radius: 6px;
  border: 1px solid var(--border-color);
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;

  &:hover {
    border-color: var(--primary-color);
    background: var(--bg-secondary);
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
  }
}

.hamburger {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 20px;

  &::before,
  &::after {
    content: '';
    width: 100%;
    height: 2px;
    background: var(--text-primary);
    border-radius: 2px;
    transition: all 0.3s;
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
