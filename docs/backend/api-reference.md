# 后端API参考文档

> 最后更新：2026-01-14
> 版本：v1.0.0
> 框架：FastAPI 0.109.0

---

## 服务配置

### 开发环境
```
后端地址：http://localhost:8000
API文档：http://localhost:8000/api/docs
```

### CORS配置
允许的前端来源（`app/config.py`）：
```python
CORS_ORIGINS = '["http://localhost:5173", "http://localhost:3000"]'
```

---

## 通用响应格式

### ApiResponse（单条数据）
```json
{
  "code": 0,
  "message": "success",
  "data": { /* 单条数据 */ }
}
```

### PaginatedResponse（分页数据）
```json
{
  "items": [/* 数据列表 */],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
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

---

## API端点详解

### 健康检查

#### GET /
根路径健康检查

**响应**：
```json
{ "code": 0, "message": "Auto Info API is running", "data": { "version": "1.0.0" } }
```

#### GET /api/health
健康检查接口

**响应**：
```json
{ "code": 0, "message": "OK", "data": { "status": "healthy" } }
```

---

### 文章API

#### GET /api/articles
获取文章列表（支持分页和筛选）

**Query参数**：
| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | int | 否 | 1 | 页码（从1开始） |
| page_size | int | 否 | 20 | 每页数量 |
| category | str | 否 | - | 分类slug筛选 |
| tag | str | 否 | - | 标签slug筛选 |
| status | str | 否 | published | 文章状态 |

**响应格式**：PaginatedResponse
```json
{
  "items": [
    {
      "id": 1,
      "title": "文章标题",
      "slug": "article-slug",
      "summary": "文章摘要",
      "cover_image": "封面图URL",
      "category": { "id": 1, "name": "分类名", "slug": "cat-slug" },
      "tags": [{ "id": 1, "name": "标签", "slug": "tag-slug" }],
      "author_name": "作者",
      "views": 100,
      "published_at": "2026-01-14T00:00:00Z",
      "created_at": "2026-01-14T00:00:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

#### GET /api/articles/{id_or_slug}
获取文章详情

**路径参数**：
- `id_or_slug`: 文章ID或slug

**响应**：ApiResponse
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "title": "文章标题",
    "slug": "article-slug",
    "summary": "摘要",
    "content": "Markdown正文内容",
    "cover_image": "封面图",
    "category": { "id": 1, "name": "分类", "slug": "slug" },
    "tags": [{ "id": 1, "name": "标签", "slug": "slug" }],
    "media_items": [
      {
        "id": 1,
        "type": "image",
        "url": "https://example.com/img.jpg",
        "thumbnail_url": "缩略图",
        "caption": "说明文字"
      }
    ],
    "author_name": "作者",
    "author_avatar": "头像URL",
    "views": 101,
    "is_original": true,
    "status": "published",
    "published_at": "2026-01-14T00:00:00Z",
    "created_at": "2026-01-14T00:00:00Z",
    "updated_at": "2026-01-14T00:00:00Z"
  }
}
```

**注意**：每次访问会自动增加 `views` 计数

#### POST /api/articles
创建文章（用于AI自动上传）

**请求头**：
```
Content-Type: application/json
```

**请求体**：
```json
{
  "title": "文章标题（必填）",
  "slug": "url-slug（可选，不填则自动生成）",
  "summary": "文章摘要",
  "content": "<h1>HTML正文内容</h1><p>这是<strong>加粗</strong>内容（必填，Quill格式）",
  "cover_image": "封面图URL",
  "category_id": 1,
  "tags": ["标签1", "标签2"],
  "author_name": "作者名",
  "author_avatar": "作者头像URL",
  "is_original": true,
  "status": "published",
  "media_items": [
    {
      "type": "image",
      "url": "https://example.com/image.jpg",
      "thumbnail_url": "缩略图",
      "caption": "图片说明",
      "order_index": 0
    }
  ],
  "published_at": "2026-01-14T00:00:00Z"
}
```

**验证规则**：
- `title`: 1-255字符
- `content`: 最少1字符
- `status`: 只能是 "draft" 或 "published"

#### PUT /api/articles/{article_id}
更新文章

**请求体**：所有字段均为可选，只更新提供的字段

#### DELETE /api/articles/{article_id}
删除文章

**注意**：级联删除关联的 media_items

---

### 分类API

#### GET /api/categories
获取所有分类

**响应**：ApiResponse
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "AI技术",
        "slug": "ai-tech",
        "description": "AI相关技术文章",
        "icon": "icon-name"
      }
    ]
  }
}
```

#### POST /api/categories
创建分类

**请求体**：
```json
{
  "name": "分类名（必填，1-50字符）",
  "slug": "url-slug（可选）",
  "description": "分类描述",
  "icon": "图标名称"
}
```

**错误**：如果分类名称已存在，返回 400 错误

---

### 标签API

#### GET /api/tags
获取所有标签

**响应**：ApiResponse
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

**Query参数**：
| 参数 | 类型 | 必填 | 默认值 |
|------|------|------|--------|
| limit | int | 否 | 20 |

**响应**：ApiResponse
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      { "id": 1, "name": "Python", "slug": "python", "count": 25 }
    ]
  }
}
```

---

### 搜索API

#### GET /api/search
搜索文章（标题或内容）

**Query参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| q | str | 是 | 搜索关键词（至少2字符） |
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |

**搜索范围**：文章标题 + 正文内容（Markdown）

**响应**：ApiResponse
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [/* 匹配的文章列表 */],
    "total": 10,
    "page": 1,
    "page_size": 20,
    "total_pages": 1,
    "keyword": "搜索词"
  }
}
```

---

### 统计API

#### GET /api/stats
获取网站统计数据

**响应**：ApiResponse
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "article_count": 100,
    "category_count": 10,
    "tag_count": 50,
    "total_views": 10000,
    "latest_articles": [
      /* 最新5篇文章 */
    ]
  }
}
```

---

## 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 认证机制

**当前版本**：未启用认证，所有API均可匿名访问

**计划中的认证**：
```python
# 预留API Key验证
API_KEY: str = "your-secret-api-key-change-this"

# 请求头格式
X-API-Key: your-secret-key
```

---

## 数据模型

### Article（文章）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| title | str(255) | 标题 |
| slug | str(255) | URL标识（唯一） |
| summary | text | 摘要 |
| content | text | Markdown正文 |
| cover_image | str(500) | 封面图 |
| category_id | int | 分类ID（外键） |
| author_name | str(100) | 作者 |
| status | str(20) | 状态：draft/published |
| is_original | bool | 是否原创 |
| views | int | 浏览次数 |
| published_at | datetime | 发布时间 |

### Category（分类）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | str(50) | 名称（唯一） |
| slug | str(50) | URL标识（唯一） |
| description | text | 描述 |
| icon | str(100) | 图标 |

### Tag（标签）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| name | str(50) | 名称（唯一） |
| slug | str(50) | URL标识（唯一） |

### Media（媒体）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键 |
| article_id | int | 文章ID（外键） |
| type | str(10) | 类型：image/video |
| url | str(500) | URL |
| thumbnail_url | str(500) | 缩略图 |
| caption | str(255) | 说明 |
| order_index | int | 排序 |

---

## 错误处理

所有错误统一返回格式：
```json
{
  "code": 错误码,
  "message": "错误描述",
  "data": null
}
```

常见错误：
- `400`: 参数验证失败、资源已存在
- `404`: 文章/分类不存在
- `500`: 服务器内部错误（生产环境不暴露详细信息）

---

## API使用示例

### Python (requests)
```python
import requests

# 获取文章列表
response = requests.get("http://localhost:8000/api/articles?page=1&page_size=10")
data = response.json()

# 创建文章
article_data = {
    "title": "新文章",
    "content": "文章内容",
    "tags": ["Python", "FastAPI"]
}
response = requests.post("http://localhost:8000/api/articles", json=article_data)
```

### JavaScript (axios)
```javascript
// 获取文章列表
const response = await axios.get('/api/articles', {
  params: { page: 1, page_size: 20 }
})

// 创建文章
const articleData = {
  title: '新文章',
  content: '文章内容',
  tags: ['Python', 'FastAPI']
}
const response = await axios.post('/api/articles', articleData)
```

### cURL
```bash
# 获取文章列表
curl http://localhost:8000/api/articles?page=1

# 创建文章
curl -X POST http://localhost:8000/api/articles \
  -H "Content-Type: application/json" \
  -d '{"title":"新文章","content":"内容","status":"published"}'
```

---

**老王API出品，接口稳如泰山！** 🐕
