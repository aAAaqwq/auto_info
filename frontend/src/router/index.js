/**
 * Vue Router 路由配置
 * 老王我按页面结构给你规划好了！
 */
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // 首页
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { title: '首页' }
  },
  // 文章列表
  {
    path: '/articles',
    name: 'ArticleList',
    component: () => import('@/views/ArticleListView.vue'),
    meta: { title: '文章库' }
  },
  // 文章详情
  {
    path: '/article/:slug',
    name: 'ArticleDetail',
    component: () => import('@/views/ArticleDetailView.vue'),
    meta: { title: '文章详情' }
  },
  // 分类页
  {
    path: '/category/:slug',
    name: 'Category',
    component: () => import('@/views/CategoryView.vue'),
    meta: { title: '分类' }
  },
  // 标签页
  {
    path: '/tag/:slug',
    name: 'Tag',
    component: () => import('@/views/TagView.vue'),
    meta: { title: '标签' }
  },
  // 搜索页
  {
    path: '/search',
    name: 'Search',
    component: () => import('@/views/SearchView.vue'),
    meta: { title: '搜索' }
  },
  // 关于页
  {
    path: '/about',
    name: 'About',
    component: () => import('@/views/AboutView.vue'),
    meta: { title: '关于' }
  },
  // 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundView.vue'),
    meta: { title: '404' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 滚动到顶部
    return { top: 0 }
  }
})

// 路由守卫 - 设置页面标题
router.beforeEach((to, from, next) => {
  const title = to.meta.title || 'Auto Info'
  document.title = `${title} - AI智能资讯`
  next()
})

export default router
