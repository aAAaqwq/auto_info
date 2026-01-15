<!-- SearchBox.vue - 可复用搜索框组件（极客风） -->
<template>
  <div class="search-box">
    <span class="search-prefix">⚡</span>
    <input
      ref="inputRef"
      v-model="searchQuery"
      type="text"
      :placeholder="placeholder"
      class="search-input"
      @keydown.enter="handleSearch"
    />
    <button class="search-btn" @click="handleSearch" :disabled="!searchQuery.trim()">
      <span class="btn-text">搜索</span>
      <span class="btn-arrow">→</span>
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

if (props.autofocus) {
  setTimeout(() => {
    inputRef.value?.focus()
  }, 100)
}

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
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 4px;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;

  // 顶部渐变线
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg,
      transparent,
      var(--accent-cyan),
      var(--primary-color),
      transparent
    );
    opacity: 0;
    transition: opacity 0.3s;
  }

  &:focus-within {
    border-color: var(--accent-cyan);
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.2);

    &::before {
      opacity: 1;
    }
  }
}

.search-prefix {
  font-size: 18px;
  padding: 0 8px 0 12px;
  opacity: 0.6;
}

.search-input {
  flex: 1;
  padding: 12px 8px;
  background: transparent;
  border: none;
  outline: none;
  font-size: 15px;
  color: var(--text-primary);
  font-family: 'JetBrains Mono', monospace;
  min-width: 0;

  &::placeholder {
    color: var(--text-tertiary);
  }
}

.search-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: linear-gradient(135deg, var(--accent-cyan), var(--primary-color));
  border: none;
  border-radius: var(--radius-md);
  color: white;
  cursor: pointer;
  font-size: 14px;
  font-family: 'JetBrains Mono', monospace;
  transition: all 0.3s;

  &:hover:not(:disabled) {
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
    transform: translateX(2px);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}

.btn-text {
  font-weight: 500;
}

.btn-arrow {
  font-size: 12px;
}
</style>
