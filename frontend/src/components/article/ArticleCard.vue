<!-- ArticleCard.vue - 文章卡片组件（极客风） -->
<template>
  <router-link :to="`/article/${article.slug}`" class="article-card">
    <!-- 极客装饰角标 -->
    <div class="card-corners">
      <span class="corner corner-tl"></span>
      <span class="corner corner-tr"></span>
      <span class="corner corner-bl"></span>
      <span class="corner corner-br"></span>
    </div>

    <!-- 封面图 -->
    <div class="card-cover" v-if="article.cover_image">
      <img :src="article.cover_image" :alt="article.title" loading="lazy" />
      <div class="card-overlay">
        <span class="read-more">
          <span class="read-icon">→</span>
          <span class="read-text">阅读全文</span>
        </span>
      </div>
      <!-- 分类标签 -->
      <div class="card-category" v-if="article.category">
        <span class="category-badge">{{ article.category.name }}</span>
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
        <div class="footer-left">
          <span class="card-author">
            <span class="author-icon">◆</span>
            {{ article.author_name }}
          </span>
          <span class="card-date">{{ formatDate(article.published_at || article.created_at) }}</span>
        </div>
        <span class="card-views" v-if="article.views">
          <span class="views-icon">👁</span>
          {{ article.views }}
        </span>
      </div>

      <!-- 标签 -->
      <div class="card-tags" v-if="article.tags?.length">
        <span class="tag" v-for="tag in article.tags.slice(0, 3)" :key="tag.id">
          <span class="tag-hash">#</span>{{ tag.name }}
        </span>
      </div>
    </div>

    <!-- 极客扫描线效果 -->
    <div class="card-scanline"></div>
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
  position: relative;
  display: block;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
  height: 100%;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg,
      var(--accent-cyan),
      var(--primary-color),
      var(--accent-purple)
    );
    opacity: 0;
    transition: opacity 0.3s;
  }

  &:hover {
    border-color: var(--border-glow);
    box-shadow: var(--shadow-glow);
    transform: translateY(-4px);

    &::before {
      opacity: 1;
    }

    .card-cover img {
      transform: scale(1.08);
    }

    .read-more {
      opacity: 1;
      transform: translateY(0);
    }

    .corner {
      opacity: 1;
    }

    .card-scanline {
      animation: scan 1.5s linear;
    }
  }
}

.card-corners {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 2;
}

.corner {
  position: absolute;
  width: 8px;
  height: 8px;
  border-color: var(--accent-cyan);
  border-style: solid;
  opacity: 0;
  transition: opacity 0.3s;

  &.corner-tl {
    top: 6px;
    left: 6px;
    border-width: 2px 0 0 2px;
  }

  &.corner-tr {
    top: 6px;
    right: 6px;
    border-width: 2px 2px 0 0;
  }

  &.corner-bl {
    bottom: 6px;
    left: 6px;
    border-width: 0 0 2px 2px;
  }

  &.corner-br {
    bottom: 6px;
    right: 6px;
    border-width: 0 2px 2px 0;
  }
}

.card-cover {
  position: relative;
  width: 100%;
  padding-top: 56.25%;
  overflow: hidden;
  background: var(--bg-tertiary);

  img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s;
  }

  .card-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top,
      rgba(15, 23, 42, 0.9) 0%,
      rgba(15, 23, 42, 0.3) 50%,
      transparent 100%
    );
    display: flex;
    align-items: flex-end;
    justify-content: center;
    padding: var(--spacing-md);
  }
}

.read-more {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg,
    var(--primary-color),
    var(--accent-purple)
  );
  color: white;
  border-radius: var(--radius-full);
  font-size: 14px;
  font-weight: 500;
  opacity: 0;
  transform: translateY(10px);
  transition: all 0.3s;
}

.read-icon {
  font-size: 16px;
}

.read-text {
  font-family: 'JetBrains Mono', monospace;
}

.card-category {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 1;
}

.category-badge {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(6, 182, 212, 0.9);
  color: white;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-radius: var(--radius-sm);
  backdrop-filter: blur(10px);
}

.card-body {
  padding: var(--spacing-md);
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.5;
  margin: 0 0 var(--spacing-sm) 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  color: var(--text-primary);
  transition: color 0.3s;

  .article-card:hover & {
    color: var(--accent-cyan);
  }
}

.card-summary {
  font-size: 14px;
  line-height: 1.6;
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
  margin-bottom: var(--spacing-sm);
}

.footer-left {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex: 1;
  min-width: 0;
}

.card-author {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.author-icon {
  color: var(--accent-purple);
  font-size: 8px;
}

.card-date {
  font-size: 11px;
  color: var(--text-tertiary);
  font-family: 'JetBrains Mono', monospace;
  white-space: nowrap;
}

.card-views {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-tertiary);
  padding: 4px 8px;
  background: var(--bg-tertiary);
  border-radius: var(--radius-sm);
}

.views-icon {
  font-size: 10px;
  opacity: 0.6;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  display: inline-flex;
  align-items: center;
  font-size: 11px;
  padding: 3px 10px;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-family: 'JetBrains Mono', monospace;
  transition: all 0.2s;

  .article-card:hover & {
    border-color: var(--accent-cyan);
    color: var(--accent-cyan);
  }

  .tag-hash {
    color: var(--accent-purple);
    margin-right: 2px;
  }
}

.card-scanline {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg,
    transparent,
    var(--accent-cyan),
    transparent
  );
  opacity: 0;
  pointer-events: none;
}

@keyframes scan {
  0% {
    top: 0;
    opacity: 0;
  }
  10% {
    opacity: 0.5;
  }
  90% {
    opacity: 0.5;
  }
  100% {
    top: 100%;
    opacity: 0;
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

  .read-more {
    padding: 8px 16px;
    font-size: 13px;
  }
}
</style>
