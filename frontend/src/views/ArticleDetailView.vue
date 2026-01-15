<!-- ArticleDetailView.vue - 文章详情页（极客风） -->
<template>
  <div class="article-detail-view">
    <div class="container" v-if="article">
      <!-- 返回按钮 -->
      <button class="back-btn" @click="router.back()">
        <span class="back-icon">←</span>
        <span class="back-text">返回</span>
      </button>

      <!-- 文章头部 -->
      <header class="article-header">
        <h1 class="article-title">{{ article.title }}</h1>

        <div class="article-meta">
          <span class="meta-item">
            <span class="meta-icon">◆</span>
            <span class="article-author">{{ article.author_name }}</span>
          </span>
          <span class="article-dot">·</span>
          <span class="meta-item">
            <span class="meta-icon">📅</span>
            <span class="article-date">{{ formatDate(article.published_at || article.created_at) }}</span>
          </span>
          <span class="article-dot">·</span>
          <span class="meta-item">
            <span class="meta-icon">👁</span>
            <span class="article-views">{{ article.views }}</span>
          </span>
        </div>

        <!-- 分类和标签 -->
        <div class="article-tags" v-if="article.category?.name || article.tags?.length">
          <router-link
            v-if="article.category"
            :to="`/category/${article.category.slug}`"
            class="category-tag"
          >
            <span class="category-icon">◈</span>
            {{ article.category.name }}
          </router-link>
          <router-link
            v-for="tag in article.tags"
            :key="tag.id"
            :to="`/tag/${tag.slug}`"
            class="tag"
          >
            <span class="tag-hash">#</span>{{ tag.name }}
          </router-link>
        </div>
      </header>

      <!-- 文章内容 -->
      <div class="article-content" v-html="article.content"></div>

      <!-- 操作按钮 -->
      <div class="article-actions">
        <button class="action-btn share-btn" @click="shareArticle">
          <span class="btn-icon">⚡</span>
          <span>分享文章</span>
        </button>
        <button class="action-btn delete-btn" @click="confirmDelete" :disabled="deleting">
          <span class="btn-icon">🗑</span>
          <span>{{ deleting ? '删除中...' : '删除文章' }}</span>
        </button>
      </div>

      <!-- 相关推荐 -->
      <ArticleRecommend
        v-if="article.id"
        :current-id="article.id"
        :tags="article.tags"
        :category="article.category"
      />
    </div>

    <!-- 加载状态 -->
    <div class="container loading" v-else-if="loading">
      <div class="loading-spinner"></div>
      <p class="loading-text">// 加载中...</p>
    </div>

    <!-- 错误状态 -->
    <div class="container error" v-else>
      <div class="error-icon">⚠</div>
      <p class="error-text">文章不存在</p>
      <router-link to="/" class="home-link">
        <span class="link-icon">⌂</span>
        返回首页
      </router-link>
    </div>

    <!-- 分享抽屉 -->
    <ShareDrawer
      :show="showShareDrawer"
      :title="article?.title || ''"
      :url="shareUrl"
      @close="showShareDrawer = false"
    />

    <!-- 阅读工具栏 -->
    <ReadingToolbar />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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
const showShareDrawer = ref(false)
const deleting = ref(false)

// 分享链接
const shareUrl = computed(() => {
  return window.location.href
})

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
  showShareDrawer.value = true
}

onMounted(() => {
  loadArticle()
})
</script>

<style lang="scss" scoped>
.article-detail-view {
  padding: var(--spacing-xl) 0 var(--spacing-2xl);
  min-height: 60vh;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: 8px 16px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  cursor: pointer;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-lg);
  transition: all 0.3s;
  font-family: 'JetBrains Mono', monospace;

  &:hover {
    border-color: var(--accent-cyan);
    color: var(--accent-cyan);
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
  }
}

.back-icon {
  font-size: 16px;
}

.article-header {
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  line-height: 1.4;
  margin: 0 0 var(--spacing-md) 0;
  color: var(--text-primary);
  font-family: 'JetBrains Mono', monospace;

  @media (max-width: 768px) {
    font-size: 24px;
  }
}

.article-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-icon {
  color: var(--accent-purple);
  font-size: 10px;
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
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: linear-gradient(135deg, var(--accent-cyan), var(--primary-color));
  color: white;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 0 15px var(--primary-glow);
    transform: translateY(-1px);
  }
}

.category-icon {
  font-size: 12px;
}

.tag {
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 13px;
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  transition: all 0.3s;

  &:hover {
    border-color: var(--accent-purple);
    color: var(--accent-purple);
    box-shadow: 0 0 10px rgba(139, 92, 246, 0.3);
  }
}

.tag-hash {
  color: var(--accent-cyan);
  margin-right: 2px;
}

.article-content {
  max-width: 800px;
  margin: 0 auto;
  font-size: 17px;
  line-height: 1.8;
  color: var(--text-primary);
  padding: 40px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 20px;
    right: 20px;
    height: 2px;
    background: linear-gradient(90deg,
      var(--accent-cyan),
      var(--primary-color),
      var(--accent-purple)
    );
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  }

  :deep(h1) {
    font-size: 28px;
    font-weight: 700;
    margin: 40px 0 20px;
    color: var(--accent-cyan);
    padding-bottom: 8px;
    border-bottom: 1px solid var(--border-color);
  }

  :deep(h2) {
    font-size: 24px;
    font-weight: 600;
    margin: 36px 0 16px;
    color: var(--text-primary);
    padding-left: 12px;
    border-left: 3px solid var(--accent-purple);
  }

  :deep(h3) {
    font-size: 20px;
    font-weight: 600;
    margin: 28px 0 12px;
    color: var(--text-primary);
  }

  :deep(h4) {
    font-size: 18px;
    font-weight: 600;
    margin: 24px 0 12px;
    color: var(--text-secondary);
  }

  :deep(p) {
    margin-bottom: 16px;
    color: var(--text-secondary);
  }

  :deep(img) {
    max-width: 100%;
    height: auto;
    margin: 24px auto;
    display: block;
    border-radius: 8px;
    border: 1px solid var(--border-color);
  }

  :deep(video) {
    max-width: 100%;
    height: auto;
    margin: 24px auto;
    display: block;
    border-radius: 8px;
    border: 1px solid var(--border-color);
  }

  :deep(iframe) {
    width: 100%;
    aspect-ratio: 16/9;
    border: none;
    border-radius: 8px;
    margin: 24px 0;
    background: #000;
  }

  :deep(pre) {
    background: var(--bg-tertiary);
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 16px 0;
    font-size: 14px;
    line-height: 1.6;
    border: 1px solid var(--border-color);
  }

  :deep(code) {
    background: rgba(139, 92, 246, 0.2);
    color: var(--accent-purple);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 14px;
    font-family: 'JetBrains Mono', Consolas, Monaco, monospace;
  }

  :deep(pre code) {
    background: transparent;
    padding: 0;
    color: var(--text-secondary);
  }

  :deep(blockquote) {
    border-left: 4px solid var(--accent-cyan);
    padding: 12px 20px;
    margin: 20px 0;
    color: var(--text-secondary);
    background: rgba(6, 182, 212, 0.05);
    border-radius: 0 8px 8px 0;
  }

  :deep(a) {
    color: var(--accent-cyan);
    text-decoration: none;
    border-bottom: 1px solid transparent;

    &:hover {
      border-bottom-color: var(--accent-cyan);
    }
  }

  :deep(ul), :deep(ol) {
    margin: 16px 0;
    padding-left: 24px;
  }

  :deep(li) {
    margin-bottom: 8px;
    color: var(--text-secondary);
  }

  :deep(table) {
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
    font-size: 15px;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    overflow: hidden;
  }

  :deep(th) {
    background: var(--bg-tertiary);
    padding: 12px;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid var(--border-color);
    color: var(--accent-cyan);
  }

  :deep(td) {
    padding: 12px;
    border-bottom: 1px solid var(--border-color);
    color: var(--text-secondary);
  }

  :deep(tr:last-child td) {
    border-bottom: none;
  }

  :deep(hr) {
    border: none;
    border-top: 1px solid var(--border-color);
    margin: 32px 0;

    &::after {
      content: '//';
      display: block;
      text-align: center;
      color: var(--text-tertiary);
      font-size: 12px;
      margin-top: -10px;
      background: var(--bg-card);
      width: fit-content;
      margin-left: auto;
      margin-right: auto;
    }
  }

  :deep(strong) {
    font-weight: 600;
    color: var(--accent-purple);
  }

  :deep(em) {
    font-style: italic;
  }
}

.article-actions {
  max-width: 800px;
  margin: var(--spacing-xl) auto 0;
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--bg-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
  font-family: 'JetBrains Mono', monospace;

  &:hover:not(:disabled) {
    border-color: var(--primary-color);
    box-shadow: 0 0 15px var(--primary-glow);
    transform: translateY(-2px);
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.share-btn .btn-icon {
  color: var(--accent-cyan);
}

.share-btn:hover:not(:disabled) {
  border-color: var(--accent-cyan);
  box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
}

.delete-btn .btn-icon {
  color: #e53e3e;
}

.delete-btn:hover:not(:disabled) {
  border-color: #e53e3e;
  box-shadow: 0 0 15px rgba(229, 62, 62, 0.4);
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl) 0;
  gap: var(--spacing-md);
}

.loading-spinner {
  width: 48px;
  height: 48px;
  border: 3px solid var(--border-color);
  border-top-color: var(--accent-cyan);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-text {
  color: var(--text-tertiary);
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error {
  text-align: center;
  padding: var(--spacing-2xl) 0;
}

.error-icon {
  font-size: 64px;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

.error-text {
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-lg) 0;
  font-size: 18px;
}

.home-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: linear-gradient(135deg, var(--primary-color), var(--accent-purple));
  color: white;
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-family: 'JetBrains Mono', monospace;
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 0 20px var(--primary-glow);
    transform: translateY(-2px);
  }
}

.link-icon {
  font-size: 16px;
}

@media (max-width: 768px) {
  .article-detail-view {
    padding: var(--spacing-lg) 0 var(--spacing-xl);
  }

  .article-content {
    padding: 20px;
    font-size: 16px;
  }

  .article-content::before {
    left: 10px;
    right: 10px;
  }

  .article-actions {
    flex-direction: column;
  }

  .article-actions .action-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
