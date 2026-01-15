<!-- ArticleListView.vue - 文章列表页 -->
<template>
  <div class="article-list-view">
    <div class="container">
      <header class="page-header">
        <h1 class="page-title">文章库</h1>
        <p class="page-subtitle">探索所有AI智能资讯</p>
      </header>

      <ArticleGrid :articles="articles" :loading="loading" />

      <div class="pagination" v-if="totalPages > 1">
        <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">上一页</button>
        <div class="page-numbers">
          <button v-for="page in visiblePages" :key="page" class="page-num" :class="{ active: page === currentPage }" @click="goToPage(page)">{{ page }}</button>
        </div>
        <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">下一页</button>
      </div>

      <div class="list-stats" v-if="!loading && total > 0">共 {{ total }} 篇文章，第 {{ currentPage }} / {{ totalPages }} 页</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'
import ArticleGrid from '@/components/article/ArticleGrid.vue'

const articleStore = useArticleStore()
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

const loadArticles = async () => {
  loading.value = true
  try {
    await articleStore.fetchArticles({ page: currentPage.value, page_size: pageSize.value })
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

onMounted(loadArticles)
</script>

<style lang="scss" scoped>
.article-list-view { padding: var(--spacing-lg) 0 var(--spacing-xl); min-height: 60vh; }
.page-header { text-align: center; margin-bottom: var(--spacing-xl); }
.page-title { font-size: 32px; font-weight: 700; color: var(--text-primary); margin: 0 0 var(--spacing-sm) 0; @media (max-width: 768px) { font-size: 24px; } }
.page-subtitle { font-size: 16px; color: var(--text-secondary); margin: 0; }
.pagination { display: flex; align-items: center; justify-content: center; gap: var(--spacing-sm); margin-top: var(--spacing-xl); flex-wrap: wrap; }
.page-btn { padding: 8px 16px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-sm); color: var(--text-primary); cursor: pointer; transition: all 0.2s;&:hover:not(:disabled) { border-color: var(--primary-color); color: var(--primary-color); }&:disabled { opacity: 0.5; cursor: not-allowed; } }
.page-numbers { display: flex; gap: 4px; }
.page-num { min-width: 36px; height: 36px; padding: 0 8px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-sm); color: var(--text-primary); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s;&:hover { border-color: var(--primary-color); color: var(--primary-color); }&.active { background: var(--primary-color); border-color: var(--primary-color); color: white; } }
.list-stats { text-align: center; margin-top: var(--spacing-lg); color: var(--text-tertiary); font-size: 14px; }
</style>