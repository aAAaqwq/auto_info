<!-- AppFooter.vue - 底部组件（架构版） -->
<template>
  <footer class="app-footer">
    <div class="container footer-inner">
      <!-- 统计信息 -->
      <div class="footer-stats">
        <span>文章数: {{ stats?.article_count || 0 }}</span>
        <span>分类数: {{ stats?.category_count || 0 }}</span>
        <span>总浏览: {{ stats?.total_views || 0 }}</span>
      </div>

      <!-- 版权信息 -->
      <div class="footer-copyright">
        <p>&copy; {{ new Date().getFullYear() }} Auto Info. AI智能资讯聚合系统</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { useAppStore } from '@/stores/app'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'

const appStore = useAppStore()
const { stats } = storeToRefs(appStore)

onMounted(() => {
  appStore.fetchStats()
})
</script>

<style lang="scss" scoped>
.app-footer {
  background: var(--bg-primary);
  border-top: 1px solid var(--border-light);
  padding: var(--spacing-lg) 0;
  margin-top: var(--spacing-xl);
}

.footer-inner {
  text-align: center;
}

.footer-stats {
  display: flex;
  justify-content: center;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
  font-size: 14px;
  color: var(--text-secondary);
}

.footer-copyright {
  font-size: 12px;
  color: var(--text-tertiary);
}

@media (max-width: 768px) {
  .footer-stats {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
}
</style>
