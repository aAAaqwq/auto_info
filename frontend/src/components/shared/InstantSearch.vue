<!-- InstantSearch.vue - 即时搜索组件 -->
<template>
  <div class="instant-search" :class="{ 'is-mobile': isMobile }">
    <!-- PC端搜索框 -->
    <div class="search-box" v-if="!isMobile || showMobileSearch">
      <input
        ref="searchInput"
        v-model="searchQuery"
        type="text"
        class="search-input"
        placeholder="搜索文章..."
        @input="onInput"
        @keydown.down="onArrowDown"
        @keydown.up="onArrowUp"
        @keydown.enter="onEnter"
        @focus="showResults = true"
        @blur="onBlur"
      />
      <span class="search-icon">🔍</span>
      <button
        v-if="isMobile"
        class="search-cancel"
        @click="closeMobileSearch"
      >取消</button>
    </div>

    <!-- 移动端搜索按钮 -->
    <button
      v-else
      class="mobile-search-trigger"
      @click="openMobileSearch"
    >
      🔍
    </button>

    <!-- 搜索建议下拉框 -->
    <transition name="dropdown">
      <div
        v-if="showResults && (loading || suggestions.length > 0 || searchQuery)"
        class="search-dropdown"
      >
        <!-- 加载中 -->
        <div v-if="loading" class="search-loading">
          <span class="spinner"></span>
          搜索中...
        </div>

        <!-- 建议列表 -->
        <ul v-else-if="suggestions.length > 0" class="suggestion-list">
          <li
            v-for="(item, index) in suggestions"
            :key="item.id"
            class="suggestion-item"
            :class="{ 'is-selected': selectedIndex === index }"
            @mousedown="goToArticle(item.slug)"
          >
            <span class="suggestion-title">{{ highlightMatch(item.title) }}</span>
            <span class="suggestion-meta">{{ item.views }} 阅读</span>
          </li>
        </ul>

        <!-- 无结果 -->
        <div v-else-if="searchQuery && !loading" class="no-results">
          没有找到 "{{ searchQuery }}"
        </div>
      </div>
    </transition>

    <!-- 移动端全屏遮罩 -->
    <transition name="fade">
      <div
        v-if="isMobile && showMobileSearch"
        class="mobile-overlay"
        @click="closeMobileSearch"
      ></div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'

const router = useRouter()
const articleStore = useArticleStore()

// 响应式判断移动端
const isMobile = ref(false)
const checkMobile = () => {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

// 搜索相关
const searchQuery = ref('')
const suggestions = ref([])
const loading = ref(false)
const showResults = ref(false)
const showMobileSearch = ref(false)
const selectedIndex = ref(-1)
const searchInput = ref(null)

// 防抖定时器
let debounceTimer = null

const onInput = () => {
  selectedIndex.value = -1

  // 清除之前的定时器
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }

  // 防抖300ms
  if (!searchQuery.value.trim()) {
    suggestions.value = []
    return
  }

  debounceTimer = setTimeout(() => {
    performSearch()
  }, 300)
}

const performSearch = async () => {
  const query = searchQuery.value.trim()
  if (!query || query.length < 2) return

  loading.value = true
  try {
    // 调用后端即时搜索API
    suggestions.value = await articleStore.instantSearch(query, 5)
  } catch (err) {
    console.error('Search failed:', err)
  } finally {
    loading.value = false
  }
}

const highlightMatch = (title) => {
  if (!searchQuery.value) return title
  const regex = new RegExp(`(${searchQuery.value})`, 'gi')
  return title.replace(regex, '<mark>$1</mark>')
}

const onArrowDown = () => {
  if (selectedIndex.value < suggestions.value.length - 1) {
    selectedIndex.value++
  }
}

const onArrowUp = () => {
  if (selectedIndex.value > 0) {
    selectedIndex.value--
  }
}

const onEnter = () => {
  if (selectedIndex.value >= 0 && suggestions.value[selectedIndex.value]) {
    goToArticle(suggestions.value[selectedIndex.value].slug)
  } else if (searchQuery.value.trim()) {
    // 跳转到搜索页
    router.push({ path: '/search', query: { q: searchQuery.value } })
    showResults.value = false
    searchQuery.value = ''
  }
}

const goToArticle = (slug) => {
  showResults.value = false
  searchQuery.value = ''
  selectedIndex.value = -1
  router.push(`/article/${slug}`)
}

const onBlur = () => {
  // 延迟关闭，让点击事件先触发
  setTimeout(() => {
    showResults.value = false
  }, 200)
}

const openMobileSearch = () => {
  showMobileSearch.value = true
  setTimeout(() => {
    searchInput.value?.focus()
  }, 100)
}

const closeMobileSearch = () => {
  showMobileSearch.value = false
  searchQuery.value = ''
  showResults.value = false
}
</script>

<style lang="scss" scoped>
.instant-search {
  position: relative;
  z-index: 100;

  &.is-mobile {
    .search-box {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      background: var(--bg-primary);
      padding: 12px 16px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      display: flex;
      align-items: center;
      gap: 12px;
    }
  }
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  padding: 10px 40px 10px 16px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  font-size: 14px;
  width: 240px;
  transition: all 0.3s;
  background: var(--bg-secondary);

  &:focus {
    outline: none;
    border-color: var(--primary-color);
    width: 300px;
    box-shadow: 0 0 0 3px rgba(var(--primary-rgb), 0.1);
  }

  .is-mobile & {
    width: 100%;
    flex: 1;

    &:focus {
      width: 100%;
    }
  }
}

.search-icon {
  position: absolute;
  right: 12px;
  color: var(--text-tertiary);
  pointer-events: none;
}

.mobile-search-trigger {
  width: 40px;
  height: 40px;
  border: none;
  background: transparent;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-cancel {
  padding: 8px 16px;
  border: none;
  background: transparent;
  color: var(--primary-color);
  cursor: pointer;
  white-space: nowrap;
}

// 搜索下拉框
.search-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  width: 100%;
  min-width: 300px;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  max-height: 400px;
  overflow-y: auto;

  .is-mobile & {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    width: 100%;
    min-width: auto;
    border-radius: 0;
    border-left: none;
    border-right: none;
    max-height: calc(100vh - 60px);
  }
}

.search-loading {
  padding: 20px;
  text-align: center;
  color: var(--text-secondary);

  .spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid var(--border-color);
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-right: 8px;
  }
}

.suggestion-list {
  list-style: none;
  margin: 0;
  padding: 8px 0;
}

.suggestion-item {
  padding: 12px 16px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.2s;

  &:hover,
  &.is-selected {
    background: var(--bg-tertiary);
  }

  &:active {
    background: var(--primary-light);
  }
}

.suggestion-title {
  flex: 1;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  mark {
    background: var(--primary-light);
    color: var(--primary-color);
    padding: 0 2px;
    border-radius: 2px;
  }
}

.suggestion-meta {
  font-size: 12px;
  color: var(--text-tertiary);
  margin-left: 12px;
  white-space: nowrap;
}

.no-results {
  padding: 20px;
  text-align: center;
  color: var(--text-secondary);
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
}

// 动画
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
  transform-origin: top right;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: scaleY(0.9);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
