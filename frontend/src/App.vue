<!-- App.vue - 根组件 -->
<template>
  <div id="app" class="app-container">
    <!-- 顶部导航栏 -->
    <AppHeader />

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 移动端侧边栏 -->
    <MobileSidebar />

    <!-- 底部 -->
    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAppStore } from '@/stores/app'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import MobileSidebar from '@/components/layout/MobileSidebar.vue'
// 初始化全局数据（分类、标签等）
const appStore = useAppStore()

onMounted(async () => {
  // 启动时加载分类列表，供导航栏使用
  await appStore.fetchCategories()
  // 初始化主题
  appStore.initTheme()
})
</script>

<style lang="scss">
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding-top: 60px; // header高度
}

// 页面切换动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
