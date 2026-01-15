<!-- HomeView.vue - 首页（极客风） -->
<template>
  <div class="home-view">
    <div class="container">
      <!-- 大图轮播 - 精选文章 -->
      <HeroCarousel :featured-articles="featuredArticles" />

      <!-- 热门标签云 -->
      <TagCloud :tags="hotTags" />

      <!-- 最新文章标题 -->
      <div class="section-header">
        <div class="header-left">
          <span class="header-icon">◈</span>
          <h2>最新文章</h2>
        </div>
        <router-link to="/articles" class="view-all">
          <span class="view-text">查看全部</span>
          <span class="view-arrow">→</span>
        </router-link>
      </div>

      <!-- 文章网格 -->
      <ArticleGrid :articles="articles" :loading="loading" />

      <!-- 加载更多 -->
      <div class="load-more" v-if="hasMore">
        <button
          class="btn btn-outline"
          @click="loadMore"
          :disabled="loadingMore"
        >
          <span v-if="loadingMore" class="loading-spinner"></span>
          {{ loadingMore ? '加载中...' : '加载更多' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'
import { useAppStore } from '@/stores/app'
import { storeToRefs } from 'pinia'
import HeroCarousel from '@/components/home/HeroCarousel.vue'
import TagCloud from '@/components/home/TagCloud.vue'
import ArticleGrid from '@/components/article/ArticleGrid.vue'

const articleStore = useArticleStore()
const appStore = useAppStore()

const { articles, pagination } = storeToRefs(articleStore)

const loading = ref(false)
const loadingMore = ref(false)

// 精选文章（取前5篇有封面的）
const featuredArticles = computed(() => {
  return articles.value
    .filter(a => a.cover_image)
    .slice(0, 5)
})

// 热门标签
const hotTags = computed(() => appStore.hotTags)

// 是否还有更多
const hasMore = computed(() => {
  return pagination.value.page < pagination.value.totalPages
})

// 加载文章列表
const loadArticles = async () => {
  loading.value = true
  try {
    await articleStore.fetchArticles()
  } finally {
    loading.value = false
  }
}

// 加载更多
const loadMore = async () => {
  if (loadingMore.value || !hasMore.value) return
  loadingMore.value = true
  try {
    articleStore.pagination.page += 1
    await articleStore.fetchArticles()
  } finally {
    loadingMore.value = false
  }
}

onMounted(async () => {
  // 并行加载文章和标签
  await Promise.all([
    loadArticles(),
    appStore.fetchHotTags(30)
  ])
})
</script>

<style lang="scss" scoped>
.home-view {
  padding: var(--spacing-xl) 0 var(--spacing-2xl);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.header-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.header-icon {
  font-size: 24px;
  color: var(--accent-cyan);
  text-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
}

h2 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
  font-family: 'JetBrains Mono', monospace;
}

.view-all {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 8px 16px;
  color: var(--text-secondary);
  font-size: 14px;
  text-decoration: none;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  transition: all 0.3s;

  &:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
    box-shadow: 0 0 15px var(--primary-glow);
  }
}

.view-text {
  font-family: 'JetBrains Mono', monospace;
}

.view-arrow {
  transition: transform 0.3s;
}

.view-all:hover .view-arrow {
  transform: translateX(4px);
}

.load-more {
  text-align: center;
  margin-top: var(--spacing-2xl);

  .btn {
    min-width: 140px;
    padding: 12px 32px;
  }
}

.loading-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .home-view {
    padding: var(--spacing-lg) 0 var(--spacing-xl);
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .view-all {
    align-self: flex-end;
  }

  .header-icon {
    font-size: 20px;
  }

  h2 {
    font-size: 20px;
  }
}
</style>
