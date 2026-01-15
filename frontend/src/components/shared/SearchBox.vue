<!-- SearchBox.vue - 可复用搜索框组件 -->
<template>
  <div class="search-box">
    <input
      ref="inputRef"
      v-model="searchQuery"
      type="text"
      :placeholder="placeholder"
      class="search-input"
      @keydown.enter="handleSearch"
    />
    <button class="search-btn" @click="handleSearch" :disabled="!searchQuery.trim()">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path
          d="M9 17A8 8 0 1 0 9 1a8 8 0 0 0 0 16zM19 19l-4.35-4.35"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '搜索文章...'
  },
  autofocus: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'search'])

const searchQuery = ref(props.modelValue)
const inputRef = ref(null)

// 自动聚焦
if (props.autofocus) {
  setTimeout(() => {
    inputRef.value?.focus()
  }, 100)
}

// 同步v-model
watch(() => props.modelValue, (newVal) => {
  searchQuery.value = newVal
})

watch(searchQuery, (newVal) => {
  emit('update:modelValue', newVal)
})

const handleSearch = () => {
  const query = searchQuery.value.trim()
  if (query) {
    emit('search', query)
  }
}

// 暴露方法供父组件调用
defineExpose({
  focus: () => inputRef.value?.focus(),
  clear: () => { searchQuery.value = '' }
})
</script>

<style lang="scss" scoped>
.search-box {
  display: flex;
  align-items: center;
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: 4px;
  transition: all 0.2s;

  &:focus-within {
    background: var(--bg-primary);
    box-shadow: 0 0 0 2px var(--primary-color);
  }
}

.search-input {
  flex: 1;
  padding: 10px 16px;
  background: transparent;
  border: none;
  outline: none;
  font-size: 15px;
  color: var(--text-primary);
  min-width: 0;

  &::placeholder {
    color: var(--text-tertiary);
  }
}

.search-btn {
  padding: 8px 16px;
  background: var(--primary-color);
  border: none;
  border-radius: var(--radius-md);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;

  &:hover:not(:disabled) {
    background: var(--primary-hover);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
</style>
