<!-- ArticleRecommend.vue - 相关文章推荐组件 -->
<template>
  <div class="article-recommend" v-if="recommendations.length > 0">
    <h3 class="recommend-title">
      <span class="title-icon">📚</span>
      相关推荐
    </h3>

    <!-- PC端：列表展示 -->
    <div class="recommend-list pc-only">
      <div
        v-for="item in recommendations"
        :key="item.id"
        class="recommend-item"
        @click="goToArticle(item.slug)"
      >
        <div class="item-cover" v-if="item.cover_image">
          <img :src="item.cover_image" :alt="item.title" loading="lazy" />
        </div>
        <div class="item-content">
          <h4 class="item-title">{{ item.title }}</h4>
          <p class="item-summary" v-if="item.summary">{{ truncateSummary(item.summary) }}</p>
          <div class="item-meta">
            <span class="item-views">👁 {{ item.views }}</span>
            <span class="item-date">{{ formatDate(item.published_at) }}</span>
            <span v-if="isRead(item.id)" class="read-badge">已读</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 移动端：横向滑动卡片 -->
    <div class="recommend-scroll mobile-only">
      <div
        v-for="item in recommendations"
        :key="item.id"
        class="recommend-card"
        @click="goToArticle(item.slug)"
      >
        <div class="card-cover" v-if="item.cover_image">
          <img :src="item.cover_image" :alt="item.title" loading="lazy" />
        </div>
        <div class="card-content">
          <h4 class="card-title">{{ item.title }}</h4>
          <span class="card-views">👁 {{ item.views }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const props = defineProps({
  // 当前文章ID（排除自己）
  currentId: {
    type: Number,
    required: true
  },
  // 当前文章标签
  tags: {
    type: Array,
    default: () => []
  },
  // 当前文章分类
  category: {
    type: Object,
    default: null
  },
  // 限制数量
  limit: {
    type: Number,
    default: 6
  }
})

const router = useRouter()
const articleStore = useArticleStore()

const recommendations = ref([])
const readHistory = ref([])

// 加载阅读历史
const loadReadHistory = () => {
  try {
    const history = localStorage.getItem('readHistory')
    if (history) {
      readHistory.value = JSON.parse(history)
    }
  } catch (e) {
    console.error('Failed to load read history:', e)
  }
}

// 保存到阅读历史
const saveToReadHistory = (article) => {
  try {
    const filtered = readHistory.value.filter(h => h.id !== article.id)
    readHistory.value = [{
      id: article.id,
      title: article.title,
      readAt: Date.now()
    }, ...filtered].slice(0, 50)
    localStorage.setItem('readHistory', JSON.stringify(readHistory.value))
  } catch (e) {
    console.error('Failed to save read history:', e)
  }
}

// 是否已读
const isRead = (id) => {
  return readHistory.value.some(h => h.id === id)
}

// 加载推荐文章
const loadRecommendations = async () => {
  try {
    loadReadHistory()

    // 调用后端相关推荐API
    const data = await articleStore.fetchRelated(props.currentId)
    
    // 合并同标签和同分类推荐，去重
    const byTag = data.by_tag || []
    const byCategory = data.by_category || []
    
    // 创建一个Set来追踪已添加的文章ID
    const seenIds = new Set()
    const combined = []
    
    // 先添加同标签文章（60%权重，放前面）
    for (const item of byTag) {
      if (!seenIds.has(item.id)) {
        seenIds.add(item.id)
        combined.push(item)
      }
    }
    
    // 再添加同分类热门文章（30%权重）
    for (const item of byCategory) {
      if (!seenIds.has(item.id) && combined.length < props.limit) {
        seenIds.add(item.id)
        combined.push(item)
      }
    }
    
    // 如果还不够，从阅读历史补充（10%权重）
    if (combined.length < props.limit) {
      const historyItems = readHistory.value
        .filter(h => !seenIds.has(h.id))
        .slice(0, props.limit - combined.length)
      
      // 从历史记录获取完整文章信息（这里简化处理，实际可能需要额外API调用）
      for (const item of historyItems) {
        if (combined.length >= props.limit) break
        combined.push({
          id: item.id,
          title: item.title,
          // 缺少完整信息，需要额外处理
        })
      }
    }
    
    recommendations.value = combined.slice(0, props.limit)
  } catch (e) {
    console.error('Failed to load recommendations:', e)
  }
}

const truncateSummary = (summary) => {
  if (!summary) return ''
  return summary.length > 60 ? summary.substring(0, 60) + '...' : summary
}

const formatDate = (date) => {
  if (!date) return ''
  return dayjs(date).fromNow()
}

const goToArticle = (slug) => {
  router.push(`/article/${slug}`)
}

onMounted(() => {
  loadRecommendations()
})

// 暴露方法供父组件调用
defineExpose({
  saveToReadHistory
})
</script>

<style lang="scss" scoped>
.article-recommend {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-light);
}

.recommend-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 var(--spacing-md) 0;
}

.title-icon {
  font-size: 20px;
}

// PC端列表
.recommend-list {
  display: grid;
  gap: var(--spacing-md);
}

.recommend-item {
  display: flex;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    background: var(--bg-tertiary);
    transform: translateX(4px);
  }
}

.item-cover {
  width: 120px;
  height: 80px;
  flex-shrink: 0;
  border-radius: var(--radius-sm);
  overflow: hidden;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.item-content {
  flex: 1;
  min-width: 0;
}

.item-title {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.item-summary {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0 0 8px 0;
  line-height: 1.5;
}

.item-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: var(--text-tertiary);
}

.read-badge {
  padding: 2px 6px;
  background: var(--primary-light);
  color: var(--primary-color);
  border-radius: 4px;
  font-size: 11px;
}

// 移动端横向滑动
.recommend-scroll {
  display: flex;
  gap: var(--spacing-md);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding-bottom: var(--spacing-sm);
  -webkit-overflow-scrolling: touch;

  &::-webkit-scrollbar {
    display: none;
  }
}

.recommend-card {
  flex: 0 0 200px;
  scroll-snap-align: start;
  background: var(--bg-secondary);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s;

  &:active {
    transform: scale(0.98);
  }
}

.card-cover {
  width: 100%;
  height: 100px;
  overflow: hidden;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.card-content {
  padding: 12px;
}

.card-title {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-views {
  font-size: 12px;
  color: var(--text-tertiary);
}

.pc-only {
  @media (max-width: 768px) {
    display: none;
  }
}

.mobile-only {
  display: none;

  @media (max-width: 768px) {
    display: flex;
  }
}
</style>
