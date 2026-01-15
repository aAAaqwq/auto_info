<!-- ArticleGrid.vue - 文章网格组件（极客风） -->
<template>
  <div class="article-grid">
    <!-- 空状态 -->
    <div class="grid-empty" v-if="!articles.length && !loading">
      <div class="empty-icon">∅</div>
      <p class="empty-text">暂无文章</p>
      <p class="empty-hint">// 请稍后再试</p>
    </div>

    <!-- 加载状态 -->
    <div class="grid-loading" v-else-if="loading">
      <div class="skeleton-card" v-for="i in 8" :key="i">
        <div class="skeleton-cover"></div>
        <div class="skeleton-content">
          <div class="skeleton-title"></div>
          <div class="skeleton-summary"></div>
          <div class="skeleton-meta"></div>
        </div>
      </div>
    </div>

    <!-- 文章列表 -->
    <template v-else>
      <ArticleCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
      />
    </template>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import ArticleCard from './ArticleCard.vue'

defineProps({
  articles: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})
</script>

<style lang="scss" scoped>
.article-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-lg);
  margin-top: var(--spacing-lg);

  @media (max-width: 1200px) {
    grid-template-columns: repeat(3, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
}

.grid-empty {
  grid-column: 1 / -1;
  text-align: center;
  padding: var(--spacing-2xl) 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
}

.empty-icon {
  font-size: 64px;
  color: var(--text-tertiary);
  opacity: 0.5;
  font-family: 'JetBrains Mono', monospace;
}

.empty-text {
  margin: 0;
  color: var(--text-secondary);
  font-size: 16px;
  font-family: 'JetBrains Mono', monospace;
}

.empty-hint {
  margin: 0;
  color: var(--text-tertiary);
  font-size: 12px;
  font-family: 'JetBrains Mono', monospace;
  opacity: 0.6;
}

.grid-loading {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-lg);

  @media (max-width: 1200px) {
    grid-template-columns: repeat(3, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.skeleton-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
  position: relative;

  // 顶部渐变线
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg,
      var(--accent-cyan),
      var(--primary-color),
      var(--accent-purple)
    );
    opacity: 0.3;
  }
}

.skeleton-cover {
  width: 100%;
  padding-top: 56.25%;
  background: linear-gradient(
    90deg,
    var(--bg-tertiary) 25%,
    var(--bg-secondary) 50%,
    var(--bg-tertiary) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.skeleton-content {
  padding: var(--spacing-md);
}

.skeleton-title {
  height: 20px;
  margin-bottom: var(--spacing-sm);
  background: linear-gradient(
    90deg,
    var(--bg-tertiary) 25%,
    var(--bg-secondary) 50%,
    var(--bg-tertiary) 75%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  animation: shimmer 1.5s infinite;
}

.skeleton-summary {
  height: 14px;
  margin-bottom: var(--spacing-sm);
  background: linear-gradient(
    90deg,
    var(--bg-tertiary) 25%,
    var(--bg-secondary) 50%,
    var(--bg-tertiary) 75%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  width: 90%;
  animation: shimmer 1.5s infinite;
  animation-delay: 0.1s;
}

.skeleton-meta {
  height: 12px;
  background: linear-gradient(
    90deg,
    var(--bg-tertiary) 25%,
    var(--bg-secondary) 50%,
    var(--bg-tertiary) 75%
  );
  background-size: 200% 100%;
  border-radius: 4px;
  width: 60%;
  animation: shimmer 1.5s infinite;
  animation-delay: 0.2s;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}
</style>
