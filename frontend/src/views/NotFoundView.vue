<!-- NotFoundView.vue - 404页（架构占位） -->
<template>
  <div class="not-found-view">
    <div class="container">
      <h1>404 - 页面不存在</h1>
      <router-link to="/">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
// 404页逻辑
</script>

<style lang="scss" scoped>
.not-found-view {
  padding: var(--spacing-lg) 0;
  text-align: center;
}
</style>
