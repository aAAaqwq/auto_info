<!-- ArticleCard.vue - 文章卡片组件 -->
<template>
  <router-link :to="`/article/${article.slug}`" class="article-card">
    <!-- 封面图 -->
    <div class="card-cover" v-if="article.cover_image">
      <img :src="article.cover_image" :alt="article.title" loading="lazy" />
      <div class="card-overlay">
        <span class="read-more">阅读更多 →</span>
      </div>
    </div>

    <!-- 卡片内容 -->
    <div class="card-body">
      <!-- 标题 -->
      <h3 class="card-title">{{ article.title }}</h3>

      <!-- 摘要 -->
      <p class="card-summary" v-if="article.summary">{{ article.summary }}</p>

      <!-- 底部信息 -->
      <div class="card-footer">
        <span class="card-author">{{ article.author_name }}</span>
        <span class="card-date">{{ formatDate(article.published_at || article.created_at) }}</span>
      </div>

      <!-- 标签 -->
      <div class="card-tags" v-if="article.tags?.length">
        <span class="tag" v-for="tag in article.tags.slice(0, 3)" :key="tag.id">
          #{{ tag.name }}
        </span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { defineProps } from 'vue'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

const formatDate = (date) => {
  if (!date) return ''
  return dayjs(date).fromNow()
}
</script>

<style lang="scss" scoped>
.article-card {
  display: block;
  background: var(--bg-primary);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;

  &:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-4px);

    .card-cover img {
      transform: scale(1.05);
    }

    .read-more {
      opacity: 1;
      transform: translateY(0);
    }
  }
}

.card-cover {
  position: relative;
  width: 100%;
  padding-top: 56.25%; // 16:9 比例
  overflow: hidden;
  background: var(--bg-tertiary);

  img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }

  .card-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.6) 0%, transparent 50%);
    display: flex;
    align-items: flex-end;
    padding: var(--spacing-md);
    opacity: 0;
    transition: opacity 0.3s ease;

    .article-card:hover & {
      opacity: 1;
    }
  }

  .read-more {
    color: white;
    font-size: 14px;
    opacity: 0;
    transform: translateY(10px);
    transition: all 0.3s ease;
  }
}

.card-body {
  padding: var(--spacing-md);
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.4;
  margin: 0 0 var(--spacing-sm) 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: var(--text-primary);
}

.card-summary {
  font-size: 14px;
  line-height: 1.5;
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-md) 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: var(--text-tertiary);
  margin-bottom: var(--spacing-sm);
}

.card-author {
  color: var(--text-secondary);
}

.card-date {
  color: var(--text-tertiary);
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);

  .tag {
    font-size: 12px;
    padding: 2px 8px;
    background: var(--primary-light);
    color: var(--primary-color);
    border-radius: var(--radius-sm);
  }
}

@media (max-width: 768px) {
  .card-title {
    font-size: 15px;
  }

  .card-summary {
    font-size: 13px;
    -webkit-line-clamp: 2;
  }
}
</style>
