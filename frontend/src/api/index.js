/**
 * API请求封装
 * 老王我用axios给你搭好了，别tm乱改！
 */
import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 这里可以添加token等
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 后端返回格式: { code: 0, message: "success", data: ... }
    return response.data
  },
  error => {
    console.error('响应错误:', error)
    return Promise.reject(error)
  }
)

// ========== 文章API ==========
export const articleApi = {
  // 获取文章列表
  getList(params) {
    return api.get('/articles', { params })
  },
  // 获取文章详情
  getDetail(idOrSlug) {
    return api.get(`/articles/${idOrSlug}`)
  },
  // 创建文章
  create(data) {
    return api.post('/articles', data)
  },
  // 更新文章
  update(id, data) {
    return api.put(`/articles/${id}`, data)
  },
  // 删除文章
  delete(id) {
    return api.delete(`/articles/${id}`)
  }
}

// ========== 分类API ==========
export const categoryApi = {
  // 获取所有分类
  getList() {
    return api.get('/categories')
  },
  // 创建分类
  create(data) {
    return api.post('/categories', data)
  }
}

// ========== 标签API ==========
export const tagApi = {
  // 获取所有标签
  getList() {
    return api.get('/tags')
  },
  // 获取热门标签
  getPopular(limit = 20) {
    return api.get('/tags/popular', { params: { limit } })
  }
}

// ========== 搜索API ==========
export const searchApi = {
  // 搜索文章
  search(keyword, params = {}) {
    return api.get('/search', { params: { q: keyword, ...params } })
  }
}

// ========== 统计API ==========
export const statsApi = {
  // 获取网站统计
  getStats() {
    return api.get('/stats')
  }
}

export default api
