# AI智能资讯聚合系统 - 前端

> Vue 3 + Vite + Pinia + Vue Router + SCSS

## 快速启动

### 前置要求
- Node.js >= 16.x
- npm >= 8.x

### 安装依赖
```bash
npm install
```

### 启动开发服务器

**Windows用户（推荐）**：
```batch
dev.bat
```
这个脚本会自动清理Vite进程，防止端口占用。

**手动启动**：
```bash
npm run dev
```

访问：http://localhost:5173

### 清理僵尸进程（Windows）
如果遇到端口占用，运行：
```batch
stop-dev.bat
```

---

## 可用脚本

| 命令 | 说明 |
|------|------|
| `npm run dev` | 启动开发服务器 |
| `npm run build` | 构建生产版本 |
| `npm run preview` | 预览构建结果 |

---

## 后端对接

### 开发环境
- 后端地址：http://localhost:8000
- API代理已配置在 `vite.config.js`

### 启动后端
```bash
cd ../backend
python -m app.main
```

或使用uvicorn：
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 项目结构

```
src/
├── api/              # API接口
│   └── index.js
├── assets/
│   └── styles/       # 全局样式
│       └── main.scss
├── components/       # 组件
│   ├── article/      # 文章组件
│   ├── home/         # 首页组件
│   ├── layout/       # 布局组件
│   └── shared/       # 共享组件
├── router/           # 路由
│   └── index.js
├── stores/           # 状态管理
│   ├── article.js
│   └── app.js
├── views/            # 页面
│   ├── HomeView.vue
│   ├── ArticleDetailView.vue
│   ├── ArticleListView.vue
│   ├── CategoryView.vue
│   ├── TagView.vue
│   ├── SearchView.vue
│   ├── AboutView.vue
│   └── NotFoundView.vue
├── App.vue
└── main.js
```

---

## 主题变量

在 `src/assets/styles/main.scss` 中定义：

```scss
:root {
  --primary-color: #3b82f6;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --border-color: #e5e7eb;
  // ...
}
```

---

## 配置说明

### Vite配置 (vite.config.js)
- 开发端口：5173
- 自动代理：`/api` -> `http://localhost:8000`
- 端口冲突时自动尝试下一个端口

### 路由配置 (src/router/index.js)
- 基础模式：hash
- 自动懒加载页面组件

---

## 开发注意事项

### Windows Vite进程问题
Vite在Windows下退出时可能残留进程，已提供：
- `dev.bat` - 启动并自动清理
- `stop-dev.bat` - 手动清理

### 组件开发规范
- 使用 `<script setup>` 语法
- 样式使用 `scoped`
- Props使用TypeScript类型定义

### API调用规范
```javascript
// 推荐：使用封装的API方法
import { articleApi } from '@/api/index'
const data = await articleApi.getList({ page: 1 })

// 不推荐：直接调用axios
```

---

## 更多文档

- [前端开发进度](../docs/frontend/progress.md)
- [API对接文档](../docs/frontend/api-reference.md)

---

## 技术栈

| 类别 | 技术 | 版本 |
|------|------|------|
| 框架 | Vue | 3.4.15 |
| 构建工具 | Vite | 5.0.11 |
| 状态管理 | Pinia | 2.1.7 |
| 路由 | Vue Router | 4.2.5 |
| HTTP客户端 | Axios | 1.6.5 |
| 富文本 | @vueup/vue-quill | 1.2.0 |
| XSS防护 | DOMPurify | 3.3.1 |
| Markdown | marked | 11.1.1 |
| 代码高亮 | highlight.js | 11.9.0 |
| 样式 | SCSS | 1.70.0 |

---

## 后端重要说明

### 优雅关闭机制
后端已实现**优雅关闭机制**（使用FastAPI lifespan），防止内存泄漏：
- 启动时初始化数据库连接
- 关闭时自动释放所有资源
- 等待现有请求完成后再关闭

### 后端测试状态
后端已完成81个单元测试，全部通过：
- Schema验证: 23个 ✅
- ORM模型: 19个 ✅
- API端点: 31个 ✅
- CRUD流程: 8个 ✅

查看后端测试文档：`backend/tests/README.md`

---
