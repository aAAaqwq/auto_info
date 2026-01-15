<!-- ArticleGrid.vue - 文章网格组件 -->
<template>
  <div class="article-grid">
    <!-- 空状态 -->
    <div class="grid-empty" v-if="!articles.length && !loading">
      <p>暂无文章</p>
    </div>

    <!-- 加载状态 -->
    <div class="grid-loading" v-else-if="loading">
      <div class="skeleton-card" v-for="i in 8" :key="i">
        <div class="skeleton-cover"></div>
        <div class="skeleton-title"></div>
        <div class="skeleton-summary"></div>
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
  padding: var(--spacing-xl) 0;
  color: var(--text-tertiary);
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
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  overflow: hidden;

  .skeleton-cover {
    width: 100%;
    padding-top: 56.25%;
    background: linear-gradient(90deg, var(--bg-tertiary) 25%, var(--bg-secondary) 50%, var(--bg-tertiary) 75%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
  }

  .skeleton-title {
    height: 20px;
    margin: var(--spacing-md);
    background: var(--bg-tertiary);
    border-radius: 4px;
  }

  .skeleton-summary {
    height: 14px;
    margin: 0 var(--spacing-md) var(--spacing-md);
    background: var(--bg-tertiary);
    border-radius: 4px;
    width: 80%;
  }
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
