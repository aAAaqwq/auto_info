<!-- HomeView.vue - 首页 -->
<template>
  <div class="home-view">
    <div class="container">
      <!-- 大图轮播 - 精选文章 -->
      <HeroCarousel :featured-articles="featuredArticles" />

      <!-- 热门标签云 -->
      <TagCloud :tags="hotTags" />

      <!-- 最新文章标题 -->
      <div class="section-header">
        <h2>最新文章</h2>
        <router-link to="/articles" class="view-all">
          查看全部 →
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
  padding: var(--spacing-lg) 0 var(--spacing-xl);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);

  h2 {
    font-size: 24px;
    font-weight: 600;
    margin: 0;
  }
}

.view-all {
  color: var(--primary-color);
  font-size: 14px;
  transition: opacity 0.2s;

  &:hover {
    opacity: 0.8;
  }
}

.load-more {
  text-align: center;
  margin-top: var(--spacing-xl);

  .btn {
    min-width: 120px;
  }
}
</style>
