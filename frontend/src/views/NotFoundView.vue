<!-- NotFoundView.vue - 404页（极客风） -->
<template>
  <div class="not-found-view">
    <div class="container">
      <div class="error-content">
        <div class="error-decoration">
          <span class="deco-line"></span>
          <span class="deco-dot">◆</span>
          <span class="deco-line"></span>
        </div>
        
        <h1 class="error-code">404</h1>
        <h2 class="error-title">页面不存在</h2>
        <p class="error-message">抱歉，您访问的页面不存在或已被删除。</p>
        
        <div class="error-actions">
          <router-link to="/" class="action-btn primary">
            <span class="btn-icon">⌂</span>
            <span>返回首页</span>
          </router-link>
          <button class="action-btn" @click="goBack">
            <span class="btn-icon">←</span>
            <span>返回上一页</span>
          </button>
        </div>

        <div class="error-art">
          <span class="art-line"></span>
          <span class="art-bracket">&lt;</span>
          <span class="art-slash">/</span>
          <span class="art-bracket">&gt;</span>
          <span class="art-line"></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}
</script>

<style lang="scss" scoped>
.not-found-view {
  padding: var(--spacing-2xl) 0;
  min-height: 60vh;
  display: flex;
  align-items: center;
}

.error-content {
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
}

.error-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xl);
}

.deco-line {
  width: 60px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--border-color), transparent);
}

.deco-dot {
  color: var(--accent-purple);
  font-size: 8px;
}

.error-code {
  font-size: 120px;
  font-weight: 700;
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple), var(--accent-pink));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  text-shadow: 0 0 60px var(--primary-glow);

  @media (max-width: 768px) {
    font-size: 80px;
  }
}

.error-title {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 var(--spacing-md) 0;
  color: var(--text-primary);
  font-family: 'JetBrains Mono', monospace;

  @media (max-width: 768px) {
    font-size: 20px;
  }
}

.error-message {
  font-size: 16px;
  color: var(--text-tertiary);
  margin: 0 0 var(--spacing-xl) 0;
}

.error-actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-2xl);
  flex-wrap: wrap;
}

.action-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 12px 24px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  text-decoration: none;
  font-size: 14px;
  font-family: 'JetBrains Mono', monospace;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    border-color: var(--accent-cyan);
    color: var(--accent-cyan);
    box-shadow: 0 0 15px rgba(6, 182, 212, 0.3);
    transform: translateY(-2px);
  }

  &.primary {
    background: linear-gradient(135deg, var(--primary-color), var(--accent-purple));
    border-color: transparent;
    color: white;

    &:hover {
      box-shadow: 0 0 20px var(--primary-glow);
    }
  }
}

.btn-icon {
  font-size: 16px;
}

.error-art {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  opacity: 0.3;
}

.art-line {
  width: 30px;
  height: 1px;
  background: var(--border-color);
}

.art-bracket {
  font-size: 20px;
  color: var(--accent-cyan);
  font-family: 'JetBrains Mono', monospace;
}

.art-slash {
  color: var(--accent-purple);
  font-size: 24px;
  font-family: 'JetBrains Mono', monospace;
}

@media (max-width: 768px) {
  .not-found-view {
    padding: var(--spacing-xl) 0;
  }

  .error-actions {
    flex-direction: column;

    .action-btn {
      width: 100%;
      justify-content: center;
    }
  }
}
</style>
