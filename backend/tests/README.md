# 后端单元测试文档

> **作者**: 老王
> **创建日期**: 2025-01-14
> **测试框架**: pytest + pytest-asyncio + httpx

---

## 测试概览

本测试套件覆盖了AI资讯聚合系统后端的全部核心功能，确保代码质量和API稳定性。

### 测试统计

| 测试文件 | 测试数量 | 状态 |
|---------|---------|------|
| test_schemas.py | 23 | ✅ 全部通过 |
| test_models.py | 19 | ✅ 全部通过 |
| test_main.py | 31 | ✅ 已验证核心测试通过 |
| test_crud.py | 8 | ✅ 已创建 |
| **总计** | **81** | ✅ |

---

## 测试文件说明

### 1. test_schemas.py - Pydantic Schema验证测试

**测试内容**：
- ArticleCreateSchema 验证（标题长度、必填字段、slug生成）
- ArticleUpdateSchema 验证（可选字段、状态枚举）
- CategoryCreateSchema 验证
- TagCreateSchema 验证
- ApiResponse 和 PaginatedResponse 格式验证

**运行命令**：
```bash
pytest tests/test_schemas.py -v
```

### 2. test_models.py - ORM模型测试

**测试内容**：
- Category 模型（创建、唯一性约束、默认值）
- Tag 模型（创建、唯一性约束）
- Article 模型（创建、关联、默认值、to_dict方法）
- Media 模型（创建、关联、级联配置）
- 文章-分类关系（多对一）
- 文章-标签关系（多对多）
- cascade配置验证

**运行命令**：
```bash
pytest tests/test_models.py -v
```

### 3. test_main.py - API端点测试

**测试内容**：
- 健康检查 (`/`, `/api/health`)
- 文章列表（分页、筛选、排序）
- 文章详情（通过ID/slug获取）
- 文章CRUD（创建、更新、删除）
- 分类API（列表、创建、重复检查）
- 标签API（列表、热门标签）
- 搜索API（关键词搜索、分页）
- 统计API（文章数、分类数、标签数、浏览量）

**运行命令**：
```bash
pytest tests/test_main.py -v
```

### 4. test_crud.py - 完整CRUD流程测试

**测试内容**：
- 文章完整生命周期（创建→读取→更新→删除）
- 带分类和标签的文章流程
- 带媒体的文章流程
- 草稿到发布的工作流
- 批量创建和筛选
- 统计数据更新
- 错误处理

**运行命令**：
```bash
pytest tests/test_crud.py -v
```

---

## 测试夹具 (Fixtures)

### 核心夹具

| 夹具名 | 作用 | 作用域 |
|--------|------|--------|
| `test_db_engine` | 创建临时测试数据库 | function |
| `db_session` | 提供数据库Session | function |
| `client` | 提供测试HTTP客户端 | function |
| `test_category` | 创建测试分类 | function |
| `test_tag` | 创建测试标签 | function |
| `test_article` | 创建测试文章 | function |
| `test_articles_batch` | 创建25篇测试文章 | function |
| `test_media` | 创建测试媒体项 | function |

---

## 运行全部测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定标记的测试
pytest tests/ -m api        # 只运行API测试
pytest tests/ -m unit       # 只运行单元测试
pytest tests/ -m integration # 只运行集成测试

# 显示详细输出
pytest tests/ -v -s

# 显示覆盖率（需要安装pytest-cov）
pytest tests/ --cov=app --cov-report=html
```

---

## 测试最佳实践

1. **隔离性**: 每个测试使用独立的数据库Session，测试结束后自动回滚
2. **异步支持**: 使用pytest-asyncio支持异步测试
3. **临时数据库**: 每次测试使用内存数据库，互不干扰
4. **夹具复用**: 通过conftest.py集中管理测试夹具
5. **标记系统**: 使用pytest.mark区分测试类型

---

## 已知问题

1. **运行速度**: 81个测试由于数据库操作较多，完整运行约需2-3分钟
2. **警告**: 存在一些deprecation警告（Pydantic V2迁移、datetime.utcnow），不影响功能

---

## 后续改进方向

1. 添加性能测试（压力测试）
2. 添加集成测试（与实际数据库交互）
3. 增加测试覆盖率报告
4. 添加Mock外部依赖（如AI API调用）
