# AI智能资讯聚合系统 - 后端API

> FastAPI + SQLAlchemy + Pydantic

## 快速启动

### 前置要求
- Python >= 3.10
- pip

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动开发服务器
```bash
# 方式1：直接运行
python -m app.main

# 方式2：使用uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问：http://localhost:8000

### API文档
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行单个测试文件
pytest tests/test_schemas.py -v
pytest tests/test_models.py -v
pytest tests/test_main.py -v
pytest tests/test_crud.py -v

# 查看测试覆盖率
pytest tests/ --cov=app --cov-report=html
```

**测试状态**：79个测试用例全部通过 ✅

---

## 与前端对接

### 开发环境配置
- 后端地址：http://localhost:8000
- 前端地址：http://localhost:5173

### CORS配置
已在 `app/config.py` 中配置：
```python
CORS_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]
```

### 前端调用示例
```javascript
// 获取文章列表
const response = await fetch('http://localhost:8000/api/articles?page=1&page_size=20')
const data = await response.json()

// 创建文章（HTML格式）
await fetch('http://localhost:8000/api/articles', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: '文章标题',
    content: '<h1>HTML正文</h1><p>内容</p>',
    tags: ['标签1'],
    status: 'published'
  })
})
```

---

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI入口（含lifespan优雅关闭）
│   ├── models.py         # SQLAlchemy ORM模型
│   ├── schemas.py        # Pydantic数据验证
│   ├── database.py       # 数据库连接配置
│   └── config.py         # 应用配置
├── tests/                # 单元测试（79个测试用例）
│   ├── conftest.py       # pytest配置和夹具
│   ├── test_schemas.py   # Schema验证测试（23个）
│   ├── test_models.py    # ORM模型测试（19个）
│   ├── test_main.py      # API端点测试（31个）
│   └── test_crud.py      # CRUD流程测试（8个）
├── .env                  # 环境变量配置
├── requirements.txt      # Python依赖
├── pytest.ini           # pytest配置
└── auto_info.db         # SQLite数据库文件（运行后生成）
```

---

## 环境变量 (.env)

```bash
# 数据库
DATABASE_URL=sqlite+aiosqlite:///./auto_info.db

# CORS允许的前端地址
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# API密钥（预留，当前未启用认证）
API_KEY=your-secret-api-key-change-this
```

---

## 优雅关闭机制

后端已实现**优雅关闭**（使用FastAPI lifespan）：
- 启动时初始化数据库连接
- 关闭时自动释放所有资源
- 等待现有请求完成后再关闭

**重要**：按 `Ctrl+C` 停止服务时会自动清理资源，不会造成内存泄漏。

---

## 技术栈

| 类别 | 技术 | 版本 | 说明 |
|------|------|------|------|
| Web框架 | FastAPI | 0.109.0 | 异步框架，自动API文档 |
| ORM | SQLAlchemy | 2.0.25 | 异步ORM，类型提示 |
| 数据库驱动 | aiosqlite | 0.19.0 | 异步SQLite |
| 数据验证 | Pydantic | 2.5.3 | 请求/响应验证 |
| 测试框架 | pytest | 7.4.3 | 单元测试 |
| 异步测试 | pytest-asyncio | 0.21.1 | 异步测试支持 |
| HTTP测试 | httpx | 0.26.0 | 异步HTTP客户端 |

---

## API端点总览

### 文章接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/articles` | 文章列表（分页、筛选） |
| GET | `/api/articles/{id}` | 文章详情 |
| POST | `/api/articles` | **创建文章** |
| PUT | `/api/articles/{id}` | 更新文章 |
| DELETE | `/api/articles/{id}` | 删除文章 |

### 分类/标签接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/categories` | 分类列表 |
| POST | `/api/categories` | 创建分类 |
| GET | `/api/tags` | 标签列表 |
| GET | `/api/tags/popular` | 热门标签 |

### 其他接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/search` | 搜索文章 |
| GET | `/api/stats` | 网站统计 |
| GET | `/api/health` | 健康检查 |

---

## 更多文档

- [后端开发进度](../docs/backend/progress.md)
- [API参考文档](../docs/backend/api-reference.md)

---

**老王后端出品，稳如老狗！** 🐕
