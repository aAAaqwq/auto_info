# 官网展示系统 - 内容格式设计

> **项目**: auto_info - AI智能资讯聚合系统
> **设计日期**: 2026-01-14
> **设计者**: 老王

---

## 一、内容存储格式

### 选择方案：HTML富文本

**理由**：
- 渲染简单，前端直接显示
- 样式控制精细
- 图片/视频嵌入标准HTML标签
- 与参考网站（机器之心）一致

---

## 二、数据库字段设计

### articles 表

| 字段 | 类型 | 说明 |
|------|------|------|
| `content` | TEXT | HTML格式的文章正文 |
| `cover_image` | VARCHAR(500) | 封面图URL |
| `summary` | TEXT | 文章摘要（可选） |

### media 表（可选，用于独立管理媒体）

| 字段 | 类型 | 说明 |
|------|------|------|
| `article_id` | INT | 关联文章ID |
| `type` | VARCHAR(10) | 'image' 或 'video' |
| `url` | VARCHAR(500) | 媒体URL |
| `caption` | VARCHAR(255) | 说明文字 |

---

## 三、HTML内容格式规范

### 3.1 文章正文格式

```html
<h2>文章标题</h2>
<p>段落文字...</p>

<!-- 图片嵌入 -->
<img src="https://cdn.example.com/image.png" alt="图片说明" />

<p>更多段落...</p>

<!-- 视频嵌入 -->
<iframe src="https://drive.google.com/file/d/{FILE_ID}/preview"
        width="100%" height="450"
        frameborder="0"
        allow="autoplay; fullscreen">
</iframe>

<p>结尾段落...</p>
```

### 3.2 图片嵌入规范

```html
<img src="{图片URL}" alt="{图片描述}" class="article-image" />
```

**要求**：
- `src`: 完整的图片URL
- `alt`: 图片描述文字（SEO友好）
- 可选 `class`: 用于样式控制

### 3.3 Google Drive视频嵌入规范

```html
<iframe src="https://drive.google.com/file/d/{FILE_ID}/preview"
        width="100%"
        height="450"
        frameborder="0"
        allow="autoplay; fullscreen"
        class="article-video">
</iframe>
```

**FILE_ID 获取方式**：
- Google Drive分享链接格式：`https://drive.google.com/file/d/{FILE_ID}/view`
- 提取 `{FILE_ID}` 部分
- 替换为 `/preview` 结尾

---

## 四、n8n工作流输出规范

### 4.1 API请求格式

**POST** `/api/articles`

```json
{
  "title": "文章标题",
  "slug": "article-slug",
  "summary": "文章摘要",
  "content": "<h2>标题</h2><p>正文...</p><img src=\"...\" /><iframe src=\"...\"></iframe>",
  "cover_image": "https://cdn.example.com/cover.jpg",
  "category_id": 1,
  "tags": ["AI", "芯片"],
  "author_name": "AI助手",
  "is_original": true,
  "status": "published",
  "media_items": [
    {
      "type": "image",
      "url": "https://cdn.example.com/image.png",
      "caption": "图片说明"
    },
    {
      "type": "video",
      "url": "https://drive.google.com/file/d/xxx/preview",
      "caption": "视频说明"
    }
  ]
}
```

### 4.2 n8n生成HTML示例

```javascript
// n8n中生成HTML的代码示例
const htmlContent = `
<h2>${title}</h2>
<p>${introduction}</p>

${images.map(img => `
<img src="${img.url}" alt="${img.description}" />
`).join('')}

<p>${mainContent}</p>

${video ? `
<iframe src="${convertToPreviewUrl(video.url)}"
        width="100%" height="450"
        frameborder="0"
        allow="autoplay; fullscreen">
</iframe>
` : ''}

<p>${conclusion}</p>
`;
```

---

## 五、前端渲染规范

### 5.1 安全处理

使用 `DOMPurify` 清理HTML，防止XSS攻击：

```javascript
import DOMPurify from 'dompurify';

const cleanHtml = DOMPurify.sanitize(article.content);
```

### 5.2 响应式样式

```css
.article-content img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  margin: 16px 0;
}

.article-content iframe {
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 8px;
  margin: 16px 0;
}

@media (max-width: 768px) {
  .article-content iframe {
    height: 300px;
  }
}
```

---

## 六、后续优化方向

1. **图片懒加载**：使用 Intersection Observer
2. **视频预加载策略**：首屏外的视频延迟加载
3. **图片CDN加速**：使用阿里云OSS/腾讯云COS
4. **视频缩略图**：从视频提取第一帧作为封面

---

## 七、前端渲染组件

### 7.1 技术选型

| 功能 | 技术方案 |
|------|----------|
| HTML渲染 | @vueup/vue-quill（只读模式） |
| 安全清理 | DOMPurify |
| 代码高亮 | highlight.js |

### 7.2 组件结构

```
ArticleDetailView.vue
├── ArticleHeader.vue    # 标题、作者、时间
├── QuillEditor          # Quill只读渲染
├── ArticleTags.vue      # 标签列表
└── ArticleRelated.vue   # 相关推荐
```

### 7.3 Quill配置示例

```vue
<template>
  <QuillReader
    :content="article.content"
    :modules="[]"
    theme="bubble"
    :read-only="true"
  />
</template>

<script setup>
import { QuillReader } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css'
</script>
```

---

## 八、首页布局设计

### 8.1 布局风格

**大图轮播 + 网格卡片**（参考机器之心）

```
┌─────────────────────────────────────────────────────────────┐
│  [Logo] 首页 文章库 分类1 分类2 ...              [搜索] [菜单] │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │            [精选文章 - 大图轮播]                     │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  热门标签: #AI #芯片 #前端 #后端 ...                  │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐                              │
│  │卡片│ │卡片│ │卡片│ │卡片│  ← 4列网格                    │
│  └────┘ └────┘ └────┘ └────┘                              │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 组件结构

```
HomeView.vue
├── HeroCarousel.vue     # 大图轮播（精选文章）
├── TagCloud.vue         # 热门标签云
└── ArticleGrid.vue      # 文章卡片网格
    └── ArticleCard.vue  # 单个文章卡片
```

### 8.3 响应式断点

| 断点 | 屏幕宽度 | 卡片列数 |
|------|----------|----------|
| 手机 | <768px | 1列 |
| 平板 | 768-1200px | 3列 |
| PC | >1200px | 4列 |

---

## 九、依赖清单

### 前端依赖

```json
{
  "dependencies": {
    "@vueup/vue-quill": "^1.2.0",
    "dompurify": "^3.0.8",
    "highlight.js": "^11.9.0"
  }
}
```

### 后端依赖

```
已配置，无需额外依赖
```

---

**设计版本**: v1.1
**最后更新**: 2026-01-14
