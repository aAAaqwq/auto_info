<!-- ReadingToolbar.vue - 阅读工具栏组件 -->
<template>
  <div class="reading-toolbar">
    <!-- PC端固定工具栏 -->
    <div class="toolbar-pc">
      <div class="toolbar-group">
        <span class="group-label">字号</span>
        <button
          class="tool-btn"
          :class="{ active: fontSize === 'small' }"
          @click="$emit('changeFontSize', 'small')"
          title="小号"
        >A-</button>
        <button
          class="tool-btn"
          :class="{ active: fontSize === 'medium' }"
          @click="$emit('changeFontSize', 'medium')"
          title="中号"
        >A</button>
        <button
          class="tool-btn"
          :class="{ active: fontSize === 'large' }"
          @click="$emit('changeFontSize', 'large')"
          title="大号"
        >A+</button>
      </div>

      <div class="toolbar-group">
        <button
          class="tool-btn"
          :class="{ active: darkMode }"
          @click="$emit('toggleDarkMode')"
          :title="darkMode ? '关闭暗黑模式' : '开启暗黑模式'"
        >
          {{ darkMode ? '☀️' : '🌙' }}
        </button>
      </div>
    </div>

    <!-- 移动端悬浮球 -->
    <button
      class="floating-ball mobile-only"
      :class="{ 'is-expanded': isExpanded }"
      @click="toggleExpand"
    >
      <span class="ball-icon">{{ isExpanded ? '✕' : '⚙️' }}</span>

      <!-- 展开后的工具菜单 -->
      <transition name="expand">
        <div v-if="isExpanded" class="ball-menu">
          <div class="menu-item" @click.stop="$emit('changeFontSize', 'small')">
            <span class="menu-icon">A-</span>
            <span class="menu-label">小号</span>
          </div>
          <div class="menu-item" @click.stop="$emit('changeFontSize', 'medium')">
            <span class="menu-icon">A</span>
            <span class="menu-label">中号</span>
          </div>
          <div class="menu-item" @click.stop="$emit('changeFontSize', 'large')">
            <span class="menu-icon">A+</span>
            <span class="menu-label">大号</span>
          </div>
          <div class="menu-divider"></div>
          <div class="menu-item" @click.stop="toggleDarkModeClick">
            <span class="menu-icon">{{ darkMode ? '☀️' : '🌙' }}</span>
            <span class="menu-label">{{ darkMode ? '日间' : '夜间' }}</span>
          </div>
        </div>
      </transition>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  fontSize: {
    type: String,
    default: 'medium'
  },
  darkMode: {
    type: Boolean,
    default: false
  }
})

defineEmits(['changeFontSize', 'toggleDarkMode'])

const isExpanded = ref(false)

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
}

const toggleDarkModeClick = () => {
  isExpanded.value = false
  // 父组件会处理切换
}
</script>

<style lang="scss" scoped>
.reading-toolbar {
  position: fixed;
  z-index: 90;
}

// PC端工具栏
.toolbar-pc {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.toolbar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-light);

  &:last-child {
    border-bottom: none;
    padding-bottom: 0;
  }
}

.group-label {
  font-size: 11px;
  color: var(--text-tertiary);
}

.tool-btn {
  width: 36px;
  height: 36px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  background: transparent;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    background: var(--bg-secondary);
    border-color: var(--primary-color);
  }

  &.active {
    background: var(--primary-color);
    color: white;
    border-color: var(--primary-color);
  }
}

// 移动端悬浮球
.floating-ball {
  position: fixed;
  right: 20px;
  bottom: 100px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--primary-color);
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  z-index: 90;
  transition: transform 0.3s, box-shadow 0.3s;

  &:active {
    transform: scale(0.95);
  }

  &.is-expanded {
    background: var(--text-primary);
  }
}

.ball-icon {
  font-size: 20px;
  color: white;
}

.ball-menu {
  position: absolute;
  right: 0;
  bottom: 60px;
  background: var(--bg-primary);
  border-radius: var(--radius-lg);
  padding: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 140px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.2s;

  &:hover {
    background: var(--bg-secondary);
  }
}

.menu-icon {
  font-size: 16px;
}

.menu-label {
  font-size: 14px;
  color: var(--text-primary);
}

.menu-divider {
  height: 1px;
  background: var(--border-light);
  margin: 8px 0;
}

.pc-only {
  @media (max-width: 768px) {
    display: none;
  }
}

.mobile-only {
  display: none;

  @media (max-width: 768px) {
    display: block;
  }
}

// 动画
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
  transform-origin: bottom right;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: scale(0.8);
}
</style>
