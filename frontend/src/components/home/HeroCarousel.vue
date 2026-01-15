<!-- HeroCarousel.vue - 首页大图轮播组件 -->
<template>
  <div class="hero-carousel" v-if="featuredArticles.length">
    <div class="carousel-container">
      <!-- 轮播内容 -->
      <div class="carousel-track" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
        <div
          class="carousel-item"
          v-for="(article, index) in displayArticles"
          :key="article.id"
        >
          <router-link :to="`/article/${article.slug}`" class="item-link">
            <!-- 背景图 -->
            <div class="item-bg">
              <img :src="article.cover_image" :alt="article.title" />
              <div class="item-overlay"></div>
            </div>

            <!-- 内容 -->
            <div class="item-content">
              <span class="item-category" v-if="article.category">
                {{ article.category.name }}
              </span>
              <h2 class="item-title">{{ article.title }}</h2>
              <p class="item-summary" v-if="article.summary">{{ article.summary }}</p>
              <span class="item-meta">{{ article.author_name }} · {{ formatDate(article.published_at) }}</span>
            </div>
          </router-link>
        </div>
      </div>

      <!-- 导航点 -->
      <div class="carousel-dots">
        <button
          v-for="(article, index) in featuredArticles"
          :key="index"
          :class="{ active: index === currentIndex }"
          @click="goToSlide(index)"
        >
          <span></span>
        </button>
      </div>

      <!-- 左右箭头 -->
      <button class="carousel-arrow prev" @click="prev" v-if="featuredArticles.length > 1">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M15 18l-6-6 6-6" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
      <button class="carousel-arrow next" @click="next" v-if="featuredArticles.length > 1">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M9 18l6-6-6-6" stroke-width="2" stroke-linecap="round"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import dayjs from 'dayjs'

const props = defineProps({
  featuredArticles: {
    type: Array,
    default: () => []
  }
})

const currentIndex = ref(0)
let autoPlayTimer = null

// 循环展示，添加第一个到末尾实现无限滚动效果
const displayArticles = computed(() => {
  if (props.featuredArticles.length <= 1) return props.featuredArticles
  return [...props.featuredArticles, props.featuredArticles[0]]
})

const formatDate = (date) => {
  if (!date) return ''
  return dayjs(date).format('YYYY-MM-DD')
}

const next = () => {
  if (currentIndex.value < props.featuredArticles.length - 1) {
    currentIndex.value++
  } else {
    currentIndex.value = 0
  }
}

const prev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  } else {
    currentIndex.value = props.featuredArticles.length - 1
  }
}

const goToSlide = (index) => {
  currentIndex.value = index
}

const startAutoPlay = () => {
  autoPlayTimer = setInterval(next, 5000)
}

const stopAutoPlay = () => {
  if (autoPlayTimer) {
    clearInterval(autoPlayTimer)
    autoPlayTimer = null
  }
}

onMounted(() => {
  if (props.featuredArticles.length > 1) {
    startAutoPlay()
  }
})

onUnmounted(() => {
  stopAutoPlay()
})
</script>

<style lang="scss" scoped>
.hero-carousel {
  margin-bottom: var(--spacing-xl);
}

.carousel-container {
  position: relative;
  width: 100%;
  overflow: hidden;
  border-radius: var(--radius-lg);
}

.carousel-track {
  display: flex;
  transition: transform 0.5s ease;
}

.carousel-item {
  min-width: 100%;
  position: relative;
}

.item-link {
  display: block;
  position: relative;
  aspect-ratio: 21 / 9;
  overflow: hidden;
  border-radius: var(--radius-lg);

  @media (max-width: 768px) {
    aspect-ratio: 16 / 9;
  }
}

.item-bg {
  position: absolute;
  inset: 0;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.item-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.8) 0%, rgba(0,0,0,0.3) 50%, transparent 100%);
}

.item-content {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: var(--spacing-xl);
  color: white;

  @media (max-width: 768px) {
    padding: var(--spacing-md);
  }
}

.item-category {
  display: inline-block;
  padding: 4px 12px;
  background: var(--primary-color);
  border-radius: var(--radius-sm);
  font-size: 12px;
  margin-bottom: var(--spacing-sm);
}

.item-title {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.3;
  margin: 0 0 var(--spacing-sm) 0;
  max-width: 800px;

  @media (max-width: 768px) {
    font-size: 20px;
  }
}

.item-summary {
  font-size: 16px;
  opacity: 0.9;
  margin: 0 0 var(--spacing-sm) 0;
  max-width: 600px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;

  @media (max-width: 768px) {
    font-size: 14px;
    display: none; // 手机端隐藏摘要
  }
}

.item-meta {
  font-size: 14px;
  opacity: 0.7;
}

.carousel-dots {
  position: absolute;
  bottom: var(--spacing-md);
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: var(--spacing-sm);

  button {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    border: none;
    background: rgba(255,255,255,0.4);
    cursor: pointer;
    transition: all 0.3s;

    &.active {
      width: 24px;
      border-radius: 4px;
      background: white;
    }

    &:hover {
      background: rgba(255,255,255,0.7);
    }
  }
}

.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(10px);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.3s;
  opacity: 0;

  .carousel-container:hover & {
    opacity: 1;
  }

  &:hover {
    background: rgba(255,255,255,0.3);
  }

  &.prev {
    left: var(--spacing-md);
  }

  &.next {
    right: var(--spacing-md);
  }

  @media (max-width: 768px) {
    display: none;
  }
}
</style>
