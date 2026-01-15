<!-- AboutView.vue - 关于页（极客风） -->
<template>
  <div class="about-view">
    <div class="container">
      <header class="page-header">
        <div class="header-decoration">
          <span class="deco-line"></span>
          <span class="deco-bracket">&lt;</span>
          <span class="deco-bracket">&gt;</span>
          <span class="deco-line"></span>
        </div>
        <h1 class="page-title">关于 Auto Info</h1>
        <p class="page-subtitle">// AI智能资讯聚合系统</p>
      </header>

      <div class="about-content">
        <section class="about-section">
          <h2 class="section-title">
            <span class="section-icon">◈</span>
            项目简介
          </h2>
          <div class="section-body">
            <p>Auto Info 是一个专注于AI领域的智能资讯聚合系统，自动收集、整理和展示最新的AI技术文章、行业动态和产品资讯。</p>
            <p>系统采用现代化的技术架构，包括 FastAPI 后端和 Vue3 前端，实现了高效的自动化内容抓取、智能分类和个性化推荐功能。</p>
          </div>
        </section>

        <section class="about-section">
          <h2 class="section-title">
            <span class="section-icon">⚡</span>
            核心功能
          </h2>
          <div class="feature-grid">
            <div class="feature-card">
              <span class="feature-icon">🤖</span>
              <h3 class="feature-title">自动抓取</h3>
              <p class="feature-desc">自动从多个来源抓取AI相关文章</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">📊</span>
              <h3 class="feature-title">智能分类</h3>
              <p class="feature-desc">自动识别文章分类并添加标签</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">🔍</span>
              <h3 class="feature-title">全文搜索</h3>
              <p class="feature-desc">支持关键词快速搜索文章内容</p>
            </div>
            <div class="feature-card">
              <span class="feature-icon">📱</span>
              <h3 class="feature-title">响应式设计</h3>
              <p class="feature-desc">完美适配各种设备屏幕</p>
            </div>
          </div>
        </section>

        <section class="about-section">
          <h2 class="section-title">
            <span class="section-icon">🛠</span>
            技术栈
          </h2>
          <div class="tech-grid">
            <div class="tech-item">
              <span class="tech-name">FastAPI</span>
              <span class="tech-desc">后端框架</span>
            </div>
            <div class="tech-item">
              <span class="tech-name">Vue 3</span>
              <span class="tech-desc">前端框架</span>
            </div>
            <div class="tech-item">
              <span class="tech-name">Pinia</span>
              <span class="tech-desc">状态管理</span>
            </div>
            <div class="tech-item">
              <span class="tech-name">SQLite</span>
              <span class="tech-desc">数据库</span>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
// 关于页逻辑
</script>

<style lang="scss" scoped>
.about-view {
  padding: var(--spacing-xl) 0 var(--spacing-2xl);
  min-height: 60vh;
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-2xl);
}

.header-decoration {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.deco-line {
  width: 40px;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
}

.deco-bracket {
  color: var(--accent-purple);
  font-family: 'JetBrains Mono', monospace;
  font-size: 20px;
}

.page-title {
  font-size: 36px;
  font-weight: 700;
  margin: 0 0 var(--spacing-sm) 0;
  font-family: 'JetBrains Mono', monospace;
  background: linear-gradient(135deg, var(--accent-cyan), var(--primary-color), var(--accent-purple));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;

  @media (max-width: 768px) {
    font-size: 28px;
  }
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
  font-family: 'JetBrains Mono', monospace;
}

.about-content {
  max-width: 800px;
  margin: 0 auto;
}

.about-section {
  margin-bottom: var(--spacing-2xl);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 var(--spacing-lg) 0;
  font-family: 'JetBrains Mono', monospace;
  color: var(--text-primary);
}

.section-icon {
  font-size: 20px;
  color: var(--accent-cyan);
}

.section-body {
  color: var(--text-secondary);
  line-height: 1.8;

  p {
    margin-bottom: var(--spacing-md);
  }
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.feature-card {
  padding: var(--spacing-lg);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  text-align: center;
  transition: all 0.3s;

  &:hover {
    border-color: var(--accent-cyan);
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.2);
    transform: translateY(-4px);
  }
}

.feature-icon {
  font-size: 36px;
  margin-bottom: var(--spacing-sm);
}

.feature-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 var(--spacing-xs) 0;
  color: var(--text-primary);
}

.feature-desc {
  font-size: 14px;
  color: var(--text-tertiary);
  margin: 0;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);

  @media (max-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.tech-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  transition: all 0.3s;

  &:hover {
    border-color: var(--accent-purple);
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.3);
  }
}

.tech-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--accent-cyan);
  font-family: 'JetBrains Mono', monospace;
}

.tech-desc {
  font-size: 12px;
  color: var(--text-tertiary);
}

@media (max-width: 768px) {
  .about-view {
    padding: var(--spacing-lg) 0 var(--spacing-xl);
  }

  .section-title {
    font-size: 20px;
  }
}
</style>
