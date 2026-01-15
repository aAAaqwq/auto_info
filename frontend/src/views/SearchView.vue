<!-- SearchView.vue - 搜索页（极客风） -->
<template>
  <div class="search-view">
    <div class="container">
      <header class="page-header">
        <div class="header-decoration">
          <span class="deco-line"></span>
          <span class="deco-icon">🔍</span>
          <span class="deco-line"></span>
        </div>
        <h1 class="page-title">搜索</h1>
        <p class="page-subtitle">// 查找你感兴趣的AI资讯</p>
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
          <div class="result-badge">
            <span v-if="total > 0">
              <span class="result-icon">✓</span>
              找到 <span class="result-count">{{ total }}</span> 篇文章
            </span>
            <span v-else class="no-result">
              <span class="result-icon">✕</span>
              没有找到匹配的文章
            </span>
          </div>
          <p class="result-query" v-if="lastQuery">搜索词: {{ lastQuery }}</p>
        </div>

        <ArticleGrid :articles="articles" :loading="loading" />

        <div class="pagination" v-if="totalPages > 1">
          <button class="page-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">
            <span class="btn-icon">◀</span>
          </button>
          <div class="page-numbers">
            <button v-for="page in visiblePages" :key="page" class="page-num" :class="{ active: page === currentPage }" @click="goToPage(page)">{{ page }}</button>
          </div>
          <button class="page-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">
            <span class="btn-icon">▶</span>
          </button>
        </div>
      </div>
      <!-- 初始状态 -->
      <div class="empty-state" v-else>
        <div class="empty-icon">🔍</div>
        <p class="empty-title">开始你的探索</p>
        <p class="empty-subtitle">输入关键词搜索AI相关文章</p>
        <div class="hot-tags">
          <span class="hot-label">热门搜索:</span>
          <a href="#" @click.prevent="handleSearch('AI')" class="hot-tag">AI</a>
          <a href="#" @click.prevent="handleSearch('大模型')" class="hot-tag">大模型</a>
          <a href="#" @click.prevent="handleSearch('ChatGPT')" class="hot-tag">ChatGPT</a>
        </div>
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
.search-view {
  padding: var(--spacing-xl) 0 var(--spacing-2xl);
  min-height: 60vh;
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
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
  font-size: 20px;
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
  margin: 0 0 var(--spacing-lg) 0;
  font-family: 'JetBrains Mono', monospace;
}

.result-header {
  text-align: center;
  margin-bottom: var(--spacing-lg);
}

.result-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  margin-bottom: var(--spacing-sm);
}

.result-icon {
  font-size: 16px;
}

.result-count {
  font-weight: 700;
  color: var(--accent-cyan);
}

.no-result {
  color: var(--text-tertiary);
}

.result-query {
  color: var(--text-tertiary);
  font-size: 13px;
  font-family: 'JetBrains Mono', monospace;
  margin: 0;
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
  justify-content: center;
  width: 40px;
  height: 40px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.3s;

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

.empty-state {
  text-align: center;
  padding: var(--spacing-2xl) 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-md);
}

.empty-icon {
  font-size: 80px;
  opacity: 0.3;
  margin-bottom: var(--spacing-sm);
}

.empty-title {
  font-size: 20px;
  color: var(--text-secondary);
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
}

.empty-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.hot-tags {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
}

.hot-label {
  font-size: 13px;
  color: var(--text-tertiary);
  margin-right: var(--spacing-xs);
}

.hot-tag {
  padding: 6px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-full);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 13px;
  font-family: 'JetBrains Mono', monospace;
  transition: all 0.3s;

  &:hover {
    border-color: var(--accent-cyan);
    color: var(--accent-cyan);
    box-shadow: 0 0 10px rgba(6, 182, 212, 0.3);
  }
}

@media (max-width: 768px) {
  .search-view {
    padding: var(--spacing-lg) 0 var(--spacing-xl);
  }

  .page-title {
    font-size: 28px;
  }

  .empty-icon {
    font-size: 60px;
  }

  .hot-tags {
    flex-direction: column;
  }

  .hot-label {
    margin-right: 0;
    margin-bottom: var(--spacing-xs);
  }
}
</style>
