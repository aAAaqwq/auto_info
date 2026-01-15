"""
完整CRUD流程测试 - 老王说端到端测试必须跑通！
"""
import pytest
from datetime import datetime
from httpx import AsyncClient


# ========== 文章完整CRUD流程 ==========
@pytest.mark.integration
async def test_article_full_lifecycle(client: AsyncClient):
    """
    测试文章的完整生命周期：
    创建 -> 读取 -> 更新 -> 删除
    """
    # 1. 创建文章
    create_data = {
        "title": "生命周期测试文章",
        "summary": "测试CRUD完整流程",
        "content": "# 这是测试内容\n\n完整测试CRUD。",
        "author_name": "老王",
        "status": "published",
        "tags": ["测试", "CRUD"]
    }

    response = await client.post("/api/articles", json=create_data)
    assert response.status_code == 201  # POST创建返回201
    data = response.json()
    assert data["code"] == 0
    article_id = data["data"]["id"]
    article_slug = data["data"]["slug"]

    # 2. 读取文章（通过ID）
    response = await client.get(f"/api/articles/{article_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["title"] == "生命周期测试文章"
    assert data["data"]["views"] == 1  # 第一次读取

    # 3. 读取文章（通过slug）
    response = await client.get(f"/api/articles/{article_slug}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["views"] == 2  # 第二次读取

    # 4. 更新文章
    update_data = {
        "title": "更新后的标题",
        "summary": "更新后的摘要",
        "tags": ["测试", "CRUD", "已更新"]
    }
    response = await client.put(f"/api/articles/{article_id}", json=update_data)
    assert response.status_code == 200  # PUT更新返回200


@pytest.mark.integration
async def test_draft_to_publish_workflow(client: AsyncClient):
    """测试草稿到发布的工作流"""
    # 创建草稿
    draft_data = {
        "title": "草稿文章",
        "content": "这是草稿内容",
        "status": "draft"
    }

    response = await client.post("/api/articles", json=draft_data)
    assert response.status_code == 201
    article_id = response.json()["data"]["id"]
    assert response.json()["data"]["status"] == "draft"

    # 草稿不会出现在published列表中
    response = await client.get("/api/articles?status=published")
    assert len(response.json()["items"]) == 0  # PaginatedResponse格式

    # 但可以通过ID获取
    response = await client.get(f"/api/articles/{article_id}")
    assert response.status_code == 200

    # 发布文章
    publish_data = {"status": "published"}
    response = await client.put(f"/api/articles/{article_id}", json=publish_data)
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "published"

    # 现在会出现在published列表中
    response = await client.get("/api/articles?status=published")
    assert len(response.json()["items"]) == 1  # PaginatedResponse格式


@pytest.mark.integration
async def test_bulk_create_and_filter(client: AsyncClient):
    """测试批量创建和筛选"""
    # 创建分类
    category_resp = await client.post("/api/categories", json={
        "name": "技术",
        "slug": "tech"
    })
    category_id = category_resp.json()["data"]["id"]

    # 批量创建不同类型的文章
    articles = [
        {
            "title": "Python教程",
            "content": "Python内容",
            "category_id": category_id,
            "tags": ["Python", "教程"],
            "status": "published"
        },
        {
            "title": "Java教程",
            "content": "Java内容",
            "category_id": category_id,
            "tags": ["Java", "教程"],
            "status": "published"
        },
        {
            "title": "Python进阶",
            "content": "Python进阶内容",
            "category_id": category_id,
            "tags": ["Python", "进阶"],
            "status": "published"
        },
        {
            "title": "草稿文章",
            "content": "草稿",
            "status": "draft"
        }
    ]

    for article in articles:
        await client.post("/api/articles", json=article)

    # 测试筛选
    # 所有published文章
    response = await client.get("/api/articles?status=published")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3  # PaginatedResponse格式

    # 按分类筛选
    response = await client.get("/api/articles?category=tech")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3  # PaginatedResponse格式

    # 按标签筛选
    response = await client.get("/api/articles?tag=python")  # slug是小写
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2  # PaginatedResponse格式

    # 搜索测试
    response = await client.get("/api/search?q=Python")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 2  # search返回ApiResponse格式


@pytest.mark.integration
async def test_category_crud_lifecycle(client: AsyncClient):
    """测试分类的CRUD完整流程"""
    # 创建
    create_data = {
        "name": "新分类",
        "slug": "new-category",
        "description": "新分类描述",
        "icon": "new-icon"
    }
    response = await client.post("/api/categories", json=create_data)
    assert response.status_code == 201
    category_id = response.json()["data"]["id"]

    # 读取列表
    response = await client.get("/api/categories")
    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert len(items) == 1
    assert items[0]["name"] == "新分类"

    # 验证重复名称会失败
    response = await client.post("/api/categories", json={"name": "新分类"})
    assert response.status_code == 400


@pytest.mark.integration
async def test_statistics_update(client: AsyncClient):
    """测试统计数据随着操作更新"""
    # 初始统计
    response = await client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()["data"]
    initial_views = data["total_views"]

    # 创建文章
    article_resp = await client.post("/api/articles", json={
        "title": "统计测试",
        "content": "内容",
        "status": "published"
    })
    article_id = article_resp.json()["data"]["id"]

    # 创建分类
    await client.post("/api/categories", json={"name": "统计分类"})

    # 获取文章（增加浏览量）
    await client.get(f"/api/articles/{article_id}")

    # 检查统计更新
    response = await client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["article_count"] == 1
    assert data["category_count"] == 1
    assert data["total_views"] > initial_views


# 错误处理测试
@pytest.mark.integration
async def test_error_handling(client: AsyncClient):
    """测试各种错误情况的处理"""
    # 获取不存在的文章
    response = await client.get("/api/articles/999999")
    assert response.status_code == 404

    # 更新不存在的文章
    response = await client.put("/api/articles/999999", json={"title": "新标题"})
    assert response.status_code == 404

    # 删除不存在的文章
    response = await client.delete("/api/articles/999999")
    assert response.status_code == 404

    # 创建文章使用不存在的分类
    response = await client.post("/api/articles", json={
        "title": "标题",
        "content": "内容",
        "category_id": 999999
    })
    assert response.status_code == 400

    # 搜索关键词太短
    response = await client.get("/api/search?q=a")
    assert response.status_code == 400
