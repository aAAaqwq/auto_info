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
      <div class="article-content">
        <QuillReader
          :content="article.content"
          :read-only="true"
          theme="snow"
          :modules="[]"
          class="quill-reader"
        />
      </div>

      <!-- 分享按钮 -->
      <div class="article-actions">
        <button class="action-btn" @click="shareArticle">
          分享文章
        </button>
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticleStore } from '@/stores/article'
import { QuillReader } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
import DOMPurify from 'dompurify'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

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
                    'img', 'iframe', 'video', 'div', 'span'],
    ALLOWED_ATTR: ['href', 'src', 'alt', 'title', 'width', 'height', 'class', 'style',
                    'frameborder', 'allowfullscreen', 'allow', 'target'],
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
}

.quill-reader {
  font-size: 16px;
  line-height: 1.8;

  :deep(.ql-editor) {
    padding: 0;
    min-height: auto;
    color: var(--text-primary);
  }

  :deep(h2) {
    font-size: 24px;
    font-weight: 600;
    margin-top: var(--spacing-xl);
    margin-bottom: var(--spacing-md);
    color: var(--text-primary);
  }

  :deep(p) {
    margin-bottom: var(--spacing-md);
  }

  :deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: var(--radius-md);
    margin: var(--spacing-md) 0;
    display: block;
  }

  :deep(iframe) {
    width: 100%;
    aspect-ratio: 16 / 9;
    border: none;
    border-radius: var(--radius-md);
    margin: var(--spacing-md) 0;
    background: #000;
  }

  // 代码块样式
  :deep(pre) {
    background: var(--bg-secondary);
    padding: var(--spacing-md);
    border-radius: var(--radius-sm);
    overflow-x: auto;
    margin: var(--spacing-md) 0;
  }

  :deep(code) {
    background: var(--bg-secondary);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 14px;
  }

  // 引用样式
  :deep(blockquote) {
    border-left: 4px solid var(--primary-color);
    padding-left: var(--spacing-md);
    margin: var(--spacing-md) 0;
    color: var(--text-secondary);
  }

  // 链接样式
  :deep(a) {
    color: var(--primary-color);
    text-decoration: none;

    &:hover {
      text-decoration: underline;
    }
  }
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

  &:hover {
    background: var(--primary-hover);
  }
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
