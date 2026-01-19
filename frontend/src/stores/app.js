/**
 * Pinia Store - 应用全局状态
 */
import { defineStore } from 'pinia'
import { categoryApi, tagApi, statsApi } from '@/api'

export const useAppStore = defineStore('app', {
  state: () => ({
    // 分类列表
    categories: [],
    // 热门标签
    hotTags: [],
    // 网站统计
    stats: null,
    // 侧边栏状态
    sidebarOpen: false,
    // 搜索关键词
    searchKeyword: '',
    // 主题模式：dark/light
    isDark: true
  }),

  getters: {
    // 获取分类菜单
    categoryMenu: (state) => state.categories.map(c => ({
      id: c.id,
      name: c.name,
      slug: c.slug,
      icon: c.icon
    }))
  },

  actions: {
    // 获取分类列表
    async fetchCategories() {
      try {
        const res = await categoryApi.getList()
        this.categories = res.data?.items || []
        return this.categories
      } catch (err) {
        console.error('获取分类失败:', err)
      }
    },

    // 获取热门标签
    async fetchHotTags(limit = 20) {
      try {
        const res = await tagApi.getPopular(limit)
        this.hotTags = res.data?.items || []
        return this.hotTags
      } catch (err) {
        console.error('获取标签失败:', err)
      }
    },

    // 获取网站统计
    async fetchStats() {
      try {
        const res = await statsApi.getStats()
        this.stats = res.data
        return this.stats
      } catch (err) {
        console.error('获取统计失败:', err)
      }
    },

    // 切换侧边栏
    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },

    // 关闭侧边栏
    closeSidebar() {
      this.sidebarOpen = false
    },

    // 设置搜索关键词
    setSearchKeyword(keyword) {
      this.searchKeyword = keyword
    },

    // 初始化主题（从localStorage读取）
    initTheme() {
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme) {
        this.isDark = savedTheme === 'dark'
      } else {
        this.isDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      }
      this.applyTheme()
    },

    // 切换主题
    toggleTheme() {
      this.isDark = !this.isDark
      this.applyTheme()
      localStorage.setItem('theme', this.isDark ? 'dark' : 'light')
    },

    // 应用主题到DOM
    applyTheme() {
      const root = document.documentElement
      if (this.isDark) {
        root.setAttribute('data-theme', 'dark')
        document.body.classList.remove('light-mode')
        document.body.classList.add('dark-mode')
      } else {
        root.setAttribute('data-theme', 'light')
        document.body.classList.remove('dark-mode')
        document.body.classList.add('light-mode')
      }
    }
  }
})
