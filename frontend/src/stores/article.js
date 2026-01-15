/**
 * Pinia Store - 文章相关状态管理
 * 老王我用Pinia给你搭好了，比Vuex好用！
 */
import { defineStore } from 'pinia'
import { articleApi } from '@/api'

export const useArticleStore = defineStore('article', {
  state: () => ({
    // 文章列表
    articles: [],
    // 当前文章
    currentArticle: null,
    // 列表分页信息
    pagination: {
      total: 0,
      page: 1,
      pageSize: 20,
      totalPages: 0
    },
    // 加载状态
    loading: false,
    // 错误信息
    error: null
  }),

  getters: {
    // 已发布的文章
    publishedArticles: (state) => state.articles,
    // 获取文章总数
    totalCount: (state) => state.pagination.total
  },

  actions: {
    // 获取文章列表
    async fetchArticles(params = {}) {
      this.loading = true
      this.error = null
      try {
        const res = await articleApi.getList({
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
          status: 'published',
          ...params
        })
        this.articles = res.items || []
        this.pagination = {
          total: res.total || 0,
          page: res.page || 1,
          pageSize: res.page_size || 20,
          totalPages: res.total_pages || 0
        }
        return res
      } catch (err) {
        this.error = err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    // 获取文章详情
    async fetchArticle(idOrSlug) {
      this.loading = true
      this.error = null
      try {
        const res = await articleApi.getDetail(idOrSlug)
        this.currentArticle = res.data
        return res.data
      } catch (err) {
        this.error = err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    // 创建文章
    async createArticle(data) {
      this.loading = true
      this.error = null
      try {
        const res = await articleApi.create(data)
        return res.data
      } catch (err) {
        this.error = err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    // 重置状态
    reset() {
      this.articles = []
      this.currentArticle = null
      this.pagination = {
        total: 0,
        page: 1,
        pageSize: 20,
        totalPages: 0
      }
      this.error = null
    }
  }
})
