<!-- TagCloud.vue - 热门标签云组件 -->
<template>
  <div class="tag-cloud" v-if="tags.length">
    <h3 class="tag-cloud-title">热门话题</h3>
    <div class="tag-cloud-list">
      <router-link
        v-for="tag in tags"
        :key="tag.id"
        :to="`/tag/${tag.slug}`"
        class="tag-cloud-item"
        :class="getTagClass(tag.count)"
      >
        #{{ tag.name }}
        <span class="tag-count" v-if="showCount">({{ tag.count }})</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  tags: {
    type: Array,
    default: () => []
  },
  showCount: {
    type: Boolean,
    default: false
  }
})

// 根据文章数量返回样式类
const getTagClass = (count) => {
  if (!count) return 'tag-small'
  if (count >= 10) return 'tag-large'
  if (count >= 5) return 'tag-medium'
  return 'tag-small'
}
</script>

<style lang="scss" scoped>
.tag-cloud {
  margin-bottom: var(--spacing-xl);
}

.tag-cloud-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 var(--spacing-md) 0;
  color: var(--text-primary);
}

.tag-cloud-list {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
}

.tag-cloud-item {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 14px;
  color: var(--text-secondary);
  background: var(--bg-primary);
  border: 1px solid var(--border-light);
  transition: all 0.2s;
  text-decoration: none;

  &:hover {
    color: var(--primary-color);
    border-color: var(--primary-color);
    background: var(--primary-light);
    transform: translateY(-2px);
  }

  &.tag-large {
    font-size: 16px;
    font-weight: 600;
    padding: 8px 18px;
  }

  &.tag-medium {
    font-size: 15px;
  }

  &.tag-small {
    font-size: 13px;
  }
}

.tag-count {
  margin-left: 4px;
  font-size: 12px;
  opacity: 0.6;
}
</style>
