# 前后端API对接文档

> 最后更新：2026-01-14
> 后端版本：v1.0.0 | 前端版本：v1.0.0

---

## 服务地址配置

### 开发环境
```
前端地址：http://localhost:5173
后端地址：http://localhost:8000
API代理：/api -> http://localhost:8000/api
```

### 生产环境
```
需修改 vite.config.js 的 proxy 配置
或使用环境变量配置 API_BASE_URL
```

### CORS配置
后端已配置允许的前端来源（`backend/app/config.py`）：
```python
CORS_ORIGINS = '[
  "http://localhost:5173",
  "http://localhost:3000"
]'
```

---

## 通用响应格式

### 成功响应
```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "错误描述",
  "data": null
}
```

### 分页响应格式
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [...],      // 数据列表
    "total": 100,        // 总数
    "page": 1,           // 当前页
    "page_size": 20,     // 每页数量
    "total_pages": 5     // 总页数
  }
}
```

---

## API端点清单

### 健康检查

#### GET /api/health
检查服务健康状态

**请求**：无参数
**响应**：
```json
{ "code": 0, "message": "OK", "data": { "status": "healthy" } }
```

---

### 文章API

#### GET /api/articles
获取文章列表（支持分页和筛选）

**参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |
| category | str | 否 | 分类slug筛选 |
| tag | str | 否 | 标签slug筛选 |
| status | str | 否 | 文章状态，默认published |

**前端调用**：
```javascript
import { articleApi } from '@/api/index'
const result = await articleApi.getList({ page: 1, page_size: 20 })
```

#### GET /api/articles/{idOrSlug}
获取文章详情

**参数**：
- `idOrSlug`: 文章ID或slug

**响应**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "title": "文章标题",
    "slug": "article-slug",
    "summary": "摘要",
    "content": "Markdown正文",
    "cover_image": "封面图URL",
    "author_name": "作者",
    "views": 100,
    "published_at": "2026-01-14T00:00:00Z",
    "category": { "id": 1, "name": "分类名", "slug": "cat-slug" },
    "tags": [{ "id": 1, "name": "标签名", "slug": "tag-slug" }],
    "media_items": [...]
  }
}
```

#### POST /api/articles
创建文章（API上传用）

**请求体**：
```json
{
  "title": "标题",
  "slug": "url-slug",
  "summary": "摘要",
  "content": "Markdown内容",
  "cover_image": "封面图URL",
  "category_id": 1,
  "tags": ["标签1", "标签2"],
  "author_name": "作者名",
  "author_avatar": "头像URL",
  "is_original": true,
  "status": "published",
  "media_items": [
    { "type": "image", "url": "...", "caption": "说明" }
  ]
}
```

#### PUT /api/articles/{article_id}
更新文章

#### DELETE /api/articles/{article_id}
删除文章

---

### 分类API

#### GET /api/categories
获取所有分类

**响应**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      { "id": 1, "name": "AI技术", "slug": "ai-tech", "description": "...", "icon": "" }
    ]
  }
}
```

#### POST /api/categories
创建分类

---

### 标签API

#### GET /api/tags
获取所有标签

**响应**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      { "id": 1, "name": "ChatGPT", "slug": "chatgpt" }
    ]
  }
}
```

#### GET /api/tags/popular
获取热门标签（按文章数量排序）

**参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| limit | int | 否 | 返回数量，默认20 |

**前端调用**：
```javascript
import { tagApi } from '@/api/index'
const result = await tagApi.getPopular(20)
```

---

### 搜索API

#### GET /api/search
搜索文章

**参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | str | 是 | 搜索关键词（至少2字符） |
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |

**前端调用**：
```javascript
import { searchApi } from '@/api/index'
const result = await searchApi.search('ChatGPT', { page: 1 })
```

---

### 统计API

#### GET /api/stats
获取网站统计数据

**响应**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "article_count": 100,
    "category_count": 10,
    "tag_count": 50,
    "total_views": 10000,
    "latest_articles": [...]
  }
}
```

---

## 认证机制

当前版本**未启用认证**，所有API均可匿名访问。

### 计划中的认证方案
- API Key方式（后端已预留配置）
- 请求头格式：`X-API-Key: your-secret-key`

配置文件：`backend/app/config.py`
```python
API_KEY: str = "your-secret-api-key-change-this"
```

---

## 前端API使用示例

### Axios实例配置
```javascript
// src/api/index.js
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

// 响应拦截器统一处理
api.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API错误:', error)
    return Promise.reject(error)
  }
)
```

### 在组件中使用
```javascript
import { articleApi } from '@/api/index'
import { useArticleStore } from '@/stores/article'

const articleStore = useArticleStore()
await articleStore.fetchArticles({ page: 1 })
```

---

## API调试

### Swagger文档
访问：http://localhost:8000/api/docs

### ReDoc文档
访问：http://localhost:8000/api/redoc

### OpenAPI Schema
访问：http://localhost:8000/api/openapi.json

---

## 端口配置汇总

| 服务 | 端口 | 地址 |
|------|------|------|
| 前端开发服务器 | 5173 | http://localhost:5173 |
| 后端API服务器 | 8000 | http://localhost:8000 |
| API文档(Swagger) | 8000 | http://localhost:8000/api/docs |
| API文档(ReDoc) | 8000 | http://localhost:8000/api/redoc |

**代理配置**：前端通过 Vite proxy 将 `/api` 请求转发到后端 8000 端口。

```javascript
// vite.config.js
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```
