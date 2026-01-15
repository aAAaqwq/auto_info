<!-- CategoryView.vue - 分类页（极客风） -->
<template>
  <div class="category-view">
    <div class="container">
      <header class="page-header">
        <div class="header-decoration">
          <span class="deco-line"></span>
          <span class="deco-icon">◈</span>
          <span class="deco-line"></span>
        </div>
        <h1 class="page-title">{{ category?.name || '分类' }}</h1>
        <p class="page-subtitle" v-if="category?.description">// {{ category.description }}</p>
      </header>

      <ArticleGrid :articles="articles" :loading="loading" />

      <div class="pagination" v-if="totalPages > 1">
        <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">
          <span class="btn-icon">◀</span>
          <span class="btn-text">上一页</span>
        </button>
        <div class="page-numbers">
          <button v-for="page in visiblePages" :key="page" class="page-num" :class="{ active: page === currentPage }" @click="goToPage(page)">{{ page }}</button>
        </div>
        <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">
          <span class="btn-text">下一页</span>
          <span class="btn-icon">▶</span>
        </button>
      </div>

      <div class="list-stats" v-if="!loading && total > 0">
        <span class="stats-icon">◆</span>
        共 {{ total }} 篇文章
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { categoryApi } from '@/api'
import ArticleGrid from '@/components/article/ArticleGrid.vue'

const route = useRoute()
const articleStore = useArticleStore()

const category = ref(null)
const articles = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const totalPages = ref(0)

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 7
  const start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
  const end = Math.min(totalPages.value, start + maxVisible - 1)
  for (let i = start; i <= end; i++) pages.push(i)
  return pages
})

const loadCategory = async () => {
  try {
    const res = await categoryApi.getList()
    const slug = route.params.slug
    category.value = res.data?.items?.find(c => c.slug === slug)
  } catch (err) { console.error(err) }
}

const loadArticles = async () => {
  loading.value = true
  try {
    const res = await articleStore.fetchArticles({ 
      category: route.params.slug,
      page: currentPage.value,
      page_size: pageSize.value 
    })
    articles.value = articleStore.articles
    total.value = articleStore.pagination.total
    totalPages.value = articleStore.pagination.totalPages
  } catch (err) { console.error(err) } finally { loading.value = false }
}

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value || page === currentPage.value) return
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
  loadArticles()
}

watch(() => route.params.slug, () => {
  currentPage.value = 1
  loadCategory()
  loadArticles()
})

onMounted(() => {
  loadCategory()
  loadArticles()
})
</script>

<style lang="scss" scoped>
.category-view {
  padding: var(--spacing-xl) 0 var(--spacing-2xl);
  min-height: 60vh;
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.header-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.deco-line {
  width: 40px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
}

.deco-icon {
  color: var(--accent-cyan);
  font-size: 24px;
  text-shadow: 0 0 10px rgba(6, 182, 212, 0.5);
}

.page-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 var(--spacing-sm) 0;
  font-family: 'JetBrains Mono', monospace;
  background: linear-gradient(135deg, var(--accent-cyan), var(--primary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;

  @media (max-width: 768px) {
    font-size: 28px;
  }
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-2xl);
  flex-wrap: wrap;
}

.page-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s;
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;

  &:hover:not(:disabled) {
    border-color: var(--accent-cyan);
    color: var(--accent-cyan);
    box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
}

.btn-icon {
  font-size: 10px;
}

.page-numbers {
  display: flex;
  gap: 6px;
}

.page-num {
  min-width: 40px;
  height: 40px;
  padding: 0 8px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;

  &:hover {
    border-color: var(--accent-purple);
    color: var(--accent-purple);
  }

  &.active {
    background: linear-gradient(135deg, var(--primary-color), var(--accent-purple));
    border-color: var(--primary-color);
    color: white;
    box-shadow: 0 0 15px var(--primary-glow);
  }
}

.list-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
  color: var(--text-tertiary);
  font-size: 13px;
  font-family: 'JetBrains Mono', monospace;
}

.stats-icon {
  color: var(--accent-cyan);
  font-size: 10px;
}

@media (max-width: 768px) {
  .category-view {
    padding: var(--spacing-lg) 0 var(--spacing-xl);
  }

  .page-btn {
    padding: 8px 12px;
    font-size: 13px;
  }

  .page-num {
    min-width: 36px;
    height: 36px;
    font-size: 13px;
  }
}
</style>
