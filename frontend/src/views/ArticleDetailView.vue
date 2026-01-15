<!-- ArticleDetailView.vue - 文章详情页 -->
<template>
  <div class="article-detail-view">
    <div class="container" v-if="article">
      <!-- 返回按钮 -->
      <button class="back-btn" @click="router.back()">
        ← 返回
      </button>

      <!-- 文章头部 -->
      <header class="article-header">
        <h1 class="article-title">{{ article.title }}</h1>

        <div class="article-meta">
          <span class="article-author">{{ article.author_name }}</span>
          <span class="article-dot">·</span>
          <span class="article-date">{{ formatDate(article.published_at || article.created_at) }}</span>
          <span class="article-dot">·</span>
          <span class="article-views">{{ article.views }} 阅读</span>
        </div>

        <!-- 分类和标签 -->
        <div class="article-tags" v-if="article.category?.name || article.tags?.length">
          <span class="category-tag" v-if="article.category">
            {{ article.category.name }}
          </span>
          <router-link
            v-for="tag in article.tags"
            :key="tag.id"
            :to="`/tag/${tag.slug}`"
            class="tag"
          >
            #{{ tag.name }}
          </router-link>
        </div>
      </header>

      <!-- 文章内容 - Quill只读渲染 -->
      <div class="article-content" v-html="article.content"></div>

      <!-- 分享按钮 -->
      <div class="article-actions">
        <button class="action-btn" @click="shareArticle">
          分享文章
        </button>
        <button class="action-btn delete-btn" @click="confirmDelete" :disabled="deleting">
          删除文章
        </button>
        <span v-if="deleting" class="deleting-text">删除中...</span>
      </div>
    </div>

    <!-- 加载状态 -->
    <div class="container loading" v-else-if="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 错误状态 -->
    <div class="container error" v-else>
      <p>文章不存在</p>
      <router-link to="/" class="home-link">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import DOMPurify from 'dompurify'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'
import ArticleRecommend from '@/components/article/ArticleRecommend.vue'
import ShareDrawer from '@/components/shared/ShareDrawer.vue'
import ReadingToolbar from '@/components/shared/ReadingToolbar.vue'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const route = useRoute()
const router = useRouter()
const articleStore = useArticleStore()

const article = ref(null)
const loading = ref(true)

// 清理HTML内容，防止XSS
const sanitizedContent = (html) => {
  return DOMPurify.sanitize(html, {
    ALLOWED_TAGS: ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'strong', 'em', 'u', 's', 'a',
                    'ul', 'ol', 'li', 'blockquote', 'code', 'pre',
                    'img', 'iframe', 'video', 'source', 'div', 'span'],
    ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'width', 'height', 'class', 'style',
                    'frameborder', 'allowfullscreen', 'allow', 'target', 'controls', 'autoplay', 'loop', 'muted', 'playsinline', 'poster', 'type'],
    ALLOWED_URI_REGEXP: /^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i
  })
}

const formatDate = (date) => {
  if (!date) return ''
  return dayjs(date).fromNow()
}

const loadArticle = async () => {
  loading.value = true
  try {
    const slug = route.params.slug
    const data = await articleStore.fetchArticle(slug)
    // 清理HTML内容
    if (data?.content) {
      data.content = sanitizedContent(data.content)
    }
    article.value = data
  } catch (err) {
    console.error('Failed to load article:', err)
  } finally {
    loading.value = false
  }
}

const deleting = ref(false)

const confirmDelete = () => {
  if (confirm("确定要删除这篇文章吗？此操作不可恢复！")) {
    deleteArticle()
  }
}

const deleteArticle = async () => {
  if (deleting.value) return
  deleting.value = true
  try {
    await articleStore.deleteArticle(article.value.id)
    alert("文章删除成功！")
    router.push("/")
  } catch (err) {
    alert("删除失败：" + (err.message || "未知错误"))
  } finally {
    deleting.value = false
  }
}

const shareArticle = () => {
  if (navigator.share) {
    navigator.share({
      title: article.value.title,
      url: window.location.href
    })
  } else {
    navigator.clipboard.writeText(window.location.href)
    alert('链接已复制到剪贴板')
  }
}

onMounted(() => {
  loadArticle()
})
</script>

<style lang="scss" scoped>
.article-detail-view {
  padding: var(--spacing-lg) 0 var(--spacing-xl);
  min-height: 60vh;
}

.back-btn {
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-lg);

  &:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
  }
}

.article-header {
  margin-bottom: var(--spacing-xl);
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  line-height: 1.3;
  margin: 0 0 var(--spacing-md) 0;
  color: var(--text-primary);

  @media (max-width: 768px) {
    font-size: 24px;
  }
}

.article-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
}

.article-dot {
  color: var(--text-tertiary);
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.category-tag {
  padding: 4px 12px;
  background: var(--primary-color);
  color: white;
  border-radius: var(--radius-sm);
  font-size: 13px;
}

.tag {
  padding: 4px 12px;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  font-size: 13px;
  text-decoration: none;
  transition: all 0.2s;

  &:hover {
    background: var(--primary-light);
    color: var(--primary-color);
  }
}

.article-content {
  max-width: 800px;
  margin: 0 auto;
  font-size: 17px;
  line-height: 1.8;
  color: #333;
  padding: 32px;
  background: #fff;
  border: 1px solid #e1e4e8;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);

  :deep(h1) { font-size: 28px; font-weight: 700; margin: 40px 0 20px; color: #1a1a1a; }
  :deep(h2) { font-size: 24px; font-weight: 600; margin: 36px 0 16px; color: #1a1a1a; }
  :deep(h3) { font-size: 20px; font-weight: 600; margin: 28px 0 12px; color: #333; }
  :deep(h4) { font-size: 18px; font-weight: 600; margin: 24px 0 12px; color: #333; }
  :deep(p) { margin-bottom: 16px; }
  :deep(img) { max-width: 100%; height: auto; margin: 24px auto; display: block; border-radius: 8px; }
  :deep(video) { max-width: 100%; height: auto; margin: 24px auto; display: block; border-radius: 8px; }
  :deep(iframe) { width: 100%; aspect-ratio: 16/9; border: none; border-radius: 8px; margin: 24px 0; background: #000; }
  :deep(pre) { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow-x: auto; margin: 16px 0; font-size: 14px; line-height: 1.6; }
  :deep(code) { background: #f6f8fa; padding: 2px 6px; border-radius: 4px; font-size: 14px; font-family: Consolas, Monaco, Courier New, monospace; }
  :deep(pre code) { background: transparent; padding: 0; }
  :deep(blockquote) { border-left: 4px solid var(--primary-color); padding: 12px 20px; margin: 20px 0; color: #666; background: #f9f9f9; border-radius: 0 4px 4px 0; }
  :deep(a) { color: var(--primary-color); text-decoration: none; border-bottom: 1px solid transparent; &:hover { border-bottom-color: var(--primary-color); } }
  :deep(ul), :deep(ol) { margin: 16px 0; padding-left: 24px; }
  :deep(li) { margin-bottom: 8px; }
  :deep(table) { width: 100%; border-collapse: collapse; margin: 24px 0; font-size: 15px; }
  :deep(th) { background: #f6f8fa; padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #e1e4e8; }
  :deep(td) { padding: 12px; border-bottom: 1px solid #e1e4e8; }
  :deep(tr:last-child td) { border-bottom: none; }
  :deep(hr) { border: none; border-top: 1px solid #e1e4e8; margin: 32px 0; }
  :deep(strong) { font-weight: 600; color: #1a1a1a; }
  :deep(em) { font-style: italic; }
}



.article-actions {
  max-width: 800px;
  margin: var(--spacing-xl) auto 0;
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-light);
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

.action-btn {
  padding: 10px 24px;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
  position: relative;

  &:hover {
    background: var(--primary-hover);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.delete-btn {
  background: #e53e3e;

  &:hover {
    background: #c53030;
  }
}

.deleting-text {
  margin-left: 8px;
  font-size: 12px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl) 0;
  gap: var(--spacing-md);
  color: var(--text-secondary);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border-light);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: var(--spacing-xl) 0;
  color: var(--text-secondary);
}

.home-link {
  display: inline-block;
  margin-top: var(--spacing-md);
  padding: 10px 20px;
  background: var(--primary-color);
  color: white;
  border-radius: var(--radius-sm);
  text-decoration: none;
}
</style>
