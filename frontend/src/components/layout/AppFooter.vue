<!-- AppFooter.vue - 底部组件（极客风） -->
<template>
  <footer class="app-footer">
    <div class="container footer-inner">
      <!-- 统计信息 -->
      <div class="footer-stats">
        <div class="stat-item">
          <span class="stat-icon">📄</span>
          <span class="stat-label">文章</span>
          <span class="stat-value gradient-text">{{ stats?.article_count || 0 }}</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-icon">📁</span>
          <span class="stat-label">分类</span>
          <span class="stat-value gradient-text">{{ stats?.category_count || 0 }}</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-icon">👁</span>
          <span class="stat-label">浏览</span>
          <span class="stat-value gradient-text">{{ formatNumber(stats?.total_views || 0) }}</span>
        </div>
      </div>

      <!-- 极客装饰线 -->
      <div class="footer-divider">
        <span class="divider-line"></span>
        <span class="divider-dots">{ . . . }</span>
        <span class="divider-line"></span>
      </div>

      <!-- 版权信息 -->
      <div class="footer-copyright">
        <p class="copyright-text">
          <span class="copyright-bracket">&lt;</span>
          &copy; {{ new Date().getFullYear() }} Auto Info
          <span class="copyright-bracket">/&gt;</span>
        </p>
        <p class="copyright-sub">AI智能资讯聚合系统 // Powered by FastAPI + Vue3</p>
      </div>

      <!-- 极客装饰元素 -->
      <div class="footer-deco">
        <span class="deco-code">01001</span>
        <span class="deco-code">11010</span>
        <span class="deco-code">00111</span>
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

// 格式化数字显示
const formatNumber = (num) => {
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}
</script>

<style lang="scss" scoped>
.app-footer {
  position: relative;
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(20px);
  border-top: 1px solid var(--border-color);
  padding: var(--spacing-xl) 0 var(--spacing-lg);
  margin-top: var(--spacing-2xl);
  overflow: hidden;

  // 顶部渐变线
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg,
      transparent,
      var(--accent-cyan),
      var(--primary-color),
      var(--accent-purple),
      transparent
    );
  }

  // 背景网格装饰
  &::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 100px;
    background:
      linear-gradient(rgba(99, 102, 241, 0.02) 1px, transparent 1px),
      linear-gradient(90deg, rgba(99, 102, 241, 0.02) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
  }
}

.footer-inner {
  position: relative;
  text-align: center;
  z-index: 1;
}

// 统计卡片容器
.footer-stats {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
  flex-wrap: wrap;
}

// 单个统计项
.stat-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  transition: all 0.3s;

  &:hover {
    border-color: var(--primary-color);
    box-shadow: 0 0 20px var(--primary-glow);
    transform: translateY(-2px);
  }
}

.stat-icon {
  font-size: 18px;
  opacity: 0.8;
}

.stat-label {
  font-size: 13px;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stat-value {
  font-size: 18px;
  font-weight: 700;
}

.stat-divider {
  width: 1px;
  height: 24px;
  background: var(--border-color);
}

// 装饰分割线
.footer-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.divider-line {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg,
    transparent,
    var(--border-color),
    transparent
  );
}

.divider-dots {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  color: var(--text-tertiary);
  letter-spacing: 4px;
}

// 版权信息
.footer-copyright {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.copyright-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
}

.copyright-bracket {
  color: var(--accent-cyan);
  font-weight: 600;
}

.copyright-sub {
  font-size: 11px;
  color: var(--text-tertiary);
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
  opacity: 0.6;
}

// 极客装饰码
.footer-deco {
  position: absolute;
  bottom: var(--spacing-md);
  right: var(--spacing-md);
  display: flex;
  gap: 4px;
  opacity: 0.15;
  pointer-events: none;

  @media (max-width: 768px) {
    display: none;
  }
}

.deco-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--accent-cyan);
}

// 响应式
@media (max-width: 768px) {
  .footer-stats {
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .stat-item {
    width: 100%;
    justify-content: center;
  }

  .stat-divider {
    display: none;
  }

  .divider-line {
    width: 30px;
  }
}
</style>
