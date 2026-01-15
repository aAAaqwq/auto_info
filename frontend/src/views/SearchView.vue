<!-- SearchView.vue - 搜索页 -->
<template>
  <div class="search-view">
    <div class="container">
      <header class="page-header">
        <h1 class="page-title">搜索</h1>
        <SearchBox 
          v-model="searchQuery" 
          @search="handleSearch"
          :autofocus="true"
          placeholder="输入关键词搜索文章..."
        />
      </header>

      <!-- 搜索结果 -->
      <div v-if="hasSearched">
        <div class="result-header" v-if="!loading">
          <h2 class="result-title">
            <span v-if="total > 0">找到 {{ total }} 篇关于 "{{ lastQuery }}" 的文章</span>
            <span v-else>没有找到关于 "{{ lastQuery }}" 的文章</span>
          </h2>
        </div>

        <ArticleGrid :articles="articles" :loading="loading" />

        <div class="pagination" v-if="totalPages > 1">
          <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">上一页</button>
          <div class="page-numbers">
            <button v-for="page in visiblePages" :key="page" class="page-num" :class="{ active: page === currentPage }" @click="goToPage(page)">{{ page }}</button>
          </div>
          <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">下一页</button>
        </div>
      </div>

      <!-- 初始状态 -->
      <div class="empty-state" v-else>
        <svg width="80" height="80" viewBox="0 0 80 80" fill="none">
          <circle cx="30" cy="30" r="20" stroke="currentColor" stroke-width="3" />
          <circle cx="55" cy="50" r="12" stroke="currentColor" stroke-width="3" />
          <path d="M45 40L65 60" stroke="currentColor" stroke-width="3" stroke-linecap="round" />
        </svg>
        <p>输入关键词开始搜索</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchApi } from '@/api'
import ArticleGrid from '@/components/article/ArticleGrid.vue'
import SearchBox from '@/components/shared/SearchBox.vue'

const route = useRoute()
const router = useRouter()

const searchQuery = ref('')
const lastQuery = ref('')
const articles = ref([])
const loading = ref(false)
const hasSearched = ref(false)
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

const handleSearch = async (query) => {
  if (!query || !query.trim()) return
  
  searchQuery.value = query
  lastQuery.value = query
  hasSearched.value = true
  currentPage.value = 1
  
  await doSearch()
}

const doSearch = async () => {
  loading.value = true
  try {
    const res = await searchApi.search(lastQuery.value, {
      page: currentPage.value,
      page_size: pageSize.value
    })
    articles.value = res.data?.items || []
    total.value = res.data?.total || 0
    totalPages.value = res.data?.total_pages || 0
  } catch (err) { 
    console.error(err) 
    articles.value = []
    total.value = 0
    totalPages.value = 0
  } finally { 
    loading.value = false 
  }
}

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value || page === currentPage.value) return
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
  doSearch()
}

onMounted(() => {
  if (route.query.q) {
    searchQuery.value = route.query.q
    handleSearch(route.query.q)
  }
})
</script>

<style lang="scss" scoped>
.search-view { padding: var(--spacing-lg) 0 var(--spacing-xl); min-height: 60vh; }
.page-header { text-align: center; margin-bottom: var(--spacing-xl); max-width: 600px; margin-left: auto; margin-right: auto; }
.page-title { font-size: 32px; font-weight: 700; color: var(--text-primary); margin: 0 0 var(--spacing-lg) 0; @media (max-width: 768px) { font-size: 24px; } }
.result-header { margin-bottom: var(--spacing-lg); text-align: center; }
.result-title { font-size: 18px; color: var(--text-secondary); margin: 0; font-weight: 500; }
.pagination { display: flex; align-items: center; justify-content: center; gap: var(--spacing-sm); margin-top: var(--spacing-xl); flex-wrap: wrap; }
.page-btn { padding: 8px 16px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-sm); color: var(--text-primary); cursor: pointer; transition: all 0.2s;&:hover:not(:disabled) { border-color: var(--primary-color); color: var(--primary-color); }&:disabled { opacity: 0.5; cursor: not-allowed; } }
.page-numbers { display: flex; gap: 4px; }
.page-num { min-width: 36px; height: 36px; padding: 0 8px; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-sm); color: var(--text-primary); cursor: pointer; display: flex; align-items: center; justify-content: center; transition: all 0.2s;&:hover { border-color: var(--primary-color); color: var(--primary-color); }&.active { background: var(--primary-color); border-color: var(--primary-color); color: white; } }
.empty-state { text-align: center; padding: var(--spacing-xxl) 0; color: var(--text-tertiary); }
.empty-state svg { margin: 0 auto var(--spacing-md); opacity: 0.3; }
.empty-state p { font-size: 16px; margin: 0; }
</style>