"""
API端点测试 - 老王说要覆盖所有接口！
"""
import pytest
from datetime import datetime
from httpx import AsyncClient


# ========== 健康检查测试 ==========
@pytest.mark.api
async def test_root_endpoint(client: AsyncClient):
    """测试根路径健康检查"""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert "running" in data["message"]
    assert "data" in data
    assert data["data"]["version"] == "1.0.0"


@pytest.mark.api
async def test_health_endpoint(client: AsyncClient):
    """测试健康检查接口"""
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["message"] == "OK"
    assert data["data"]["status"] == "healthy"


# ========== 文章列表测试 ==========
@pytest.mark.api
async def test_list_articles_empty(client: AsyncClient):
    """测试空文章列表"""
    response = await client.get("/api/articles")
    assert response.status_code == 200
    data = response.json()
    # PaginatedResponse直接返回items, total等字段，不是ApiResponse格式
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["total_pages"] == 0


@pytest.mark.api
async def test_list_articles_with_data(client: AsyncClient, test_article):
    """测试获取文章列表"""
    response = await client.get("/api/articles")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total"] == 1
    assert data["items"][0]["title"] == "测试文章标题"


@pytest.mark.api
async def test_list_articles_pagination(client: AsyncClient, test_articles_batch):
    """测试分页功能"""
    # 第一页
    response = await client.get("/api/articles?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["total_pages"] == 3

    # 第二页
    response = await client.get("/api/articles?page=2&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["page"] == 2

    # 第三页（只有5篇）
    response = await client.get("/api/articles?page=3&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5


@pytest.mark.api
async def test_list_articles_by_category(client: AsyncClient, test_article, test_category):
    """测试按分类筛选"""
    response = await client.get(f"/api/articles?category={test_category.slug}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1


@pytest.mark.api
async def test_list_articles_by_tag(client: AsyncClient, test_article, test_tag):
    """测试按标签筛选"""
    response = await client.get(f"/api/articles?tag={test_tag.slug}")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1


@pytest.mark.api
async def test_list_articles_by_status(client: AsyncClient, db_session):
    """测试按状态筛选"""
    from app.models import Article

    # 创建草稿文章
    draft = Article(
        title="草稿文章",
        slug="draft-article",
        content="草稿内容",
        status="draft"
    )
    db_session.add(draft)
    await db_session.commit()

    # 默认只返回published
    response = await client.get("/api/articles?status=published")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0

    # 获取草稿
    response = await client.get("/api/articles?status=draft")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1


# ========== 文章详情测试 ==========
@pytest.mark.api
async def test_get_article_by_id(client: AsyncClient, test_article):
    """测试通过ID获取文章"""
    response = await client.get(f"/api/articles/{test_article.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["title"] == "测试文章标题"
    assert data["data"]["content"] is not None
    # 浏览次数应该增加
    assert data["data"]["views"] == 1


@pytest.mark.api
async def test_get_article_by_slug(client: AsyncClient, test_article):
    """测试通过slug获取文章"""
    response = await client.get(f"/api/articles/{test_article.slug}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["title"] == "测试文章标题"


@pytest.mark.api
async def test_get_article_not_found(client: AsyncClient):
    """测试获取不存在的文章"""
    response = await client.get("/api/articles/99999")
    assert response.status_code == 404


# ========== 创建文章测试 ==========
@pytest.mark.api
async def test_create_article(client: AsyncClient):
    """测试创建文章"""
    article_data = {
        "title": "新文章标题",
        "summary": "新文章摘要",
        "content": "# 新文章内容\n\n这是新创建的文章。",
        "author_name": "测试作者",
        "status": "published",
        "tags": ["Python", "FastAPI"]
    }

    response = await client.post("/api/articles", json=article_data)
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["title"] == "新文章标题"
    assert data["data"]["slug"] == "新文章标题"  # 应该自动生成
    assert len(data["data"]["tags"]) == 2


@pytest.mark.api
async def test_create_article_with_category(client: AsyncClient, test_category):
    """测试创建带分类的文章"""
    article_data = {
        "title": "带分类的文章",
        "content": "内容",
        "category_id": test_category.id,
        "status": "published"
    }

    response = await client.post("/api/articles", json=article_data)
    assert response.status_code == 201
    data = response.json()
    assert data["data"]["category"]["id"] == test_category.id


@pytest.mark.api
async def test_create_article_duplicate_slug(client: AsyncClient, test_article):
    """测试重复slug"""
    article_data = {
        "title": "测试文章标题",  # 同名会生成相同slug
        "content": "内容",
        "slug": test_article.slug,  # 手动指定相同slug
        "status": "published"
    }

    response = await client.post("/api/articles", json=article_data)
    assert response.status_code == 400


@pytest.mark.api
async def test_create_article_with_media(client: AsyncClient):
    """测试创建带媒体的文章"""
    article_data = {
        "title": "带媒体的文章",
        "content": "内容",
        "media_items": [
            {
                "type": "image",
                "url": "https://example.com/image1.jpg",
                "caption": "图片1"
            },
            {
                "type": "video",
                "url": "https://example.com/video.mp4",
                "thumbnail_url": "https://example.com/thumb.jpg",
                "caption": "视频1"
            }
        ],
        "status": "published"
    }

    response = await client.post("/api/articles", json=article_data)
    assert response.status_code == 201
    data = response.json()
    assert len(data["data"]["media_items"]) == 2


@pytest.mark.api
async def test_create_article_invalid_category(client: AsyncClient):
    """测试使用不存在的分类"""
    article_data = {
        "title": "文章",
        "content": "内容",
        "category_id": 99999,
        "status": "published"
    }

    response = await client.post("/api/articles", json=article_data)
    assert response.status_code == 400


# ========== 更新文章测试 ==========
@pytest.mark.api
async def test_update_article(client: AsyncClient, test_article):
    """测试更新文章"""
    update_data = {
        "title": "更新后的标题",
        "summary": "更新后的摘要"
    }

    response = await client.put(f"/api/articles/{test_article.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["title"] == "更新后的标题"
    assert data["data"]["summary"] == "更新后的摘要"


@pytest.mark.api
async def test_update_article_tags(client: AsyncClient, test_article, db_session):
    """测试更新文章标签"""
    from app.models import Tag

    # 创建新标签
    new_tag = Tag(name="新标签", slug="new-tag")
    db_session.add(new_tag)
    await db_session.commit()

    update_data = {
        "tags": ["新标签", "另一个标签"]
    }

    response = await client.put(f"/api/articles/{test_article.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["tags"]) == 2
    tag_names = [t["name"] for t in data["data"]["tags"]]
    assert "新标签" in tag_names


@pytest.mark.api
async def test_update_article_not_found(client: AsyncClient):
    """测试更新不存在的文章"""
    response = await client.put("/api/articles/99999", json={"title": "新标题"})
    assert response.status_code == 404


# ========== 删除文章测试 ==========
@pytest.mark.api
async def test_delete_article(client: AsyncClient, test_article):
    """测试删除文章"""
    response = await client.delete(f"/api/articles/{test_article.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0

    # 确认已删除
    response = await client.get(f"/api/articles/{test_article.id}")
    assert response.status_code == 404


@pytest.mark.api
async def test_delete_article_not_found(client: AsyncClient):
    """测试删除不存在的文章"""
    response = await client.delete("/api/articles/99999")
    assert response.status_code == 404


# ========== 分类API测试 ==========
@pytest.mark.api
async def test_list_categories_empty(client: AsyncClient):
    """测试空分类列表"""
    response = await client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["items"] == []


@pytest.mark.api
async def test_list_categories(client: AsyncClient, test_category):
    """测试获取分类列表"""
    response = await client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert len(data["data"]["items"]) == 1
    assert data["data"]["items"][0]["name"] == "测试分类"


@pytest.mark.api
async def test_create_category(client: AsyncClient):
    """测试创建分类"""
    category_data = {
        "name": "新分类",
        "slug": "new-category",
        "description": "新分类描述",
        "icon": "new-icon"
    }

    response = await client.post("/api/categories", json=category_data)
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["name"] == "新分类"


@pytest.mark.api
async def test_create_category_duplicate(client: AsyncClient, test_category):
    """测试创建重复分类"""
    category_data = {
        "name": "测试分类",  # 重复名称
        "description": "描述"
    }

    response = await client.post("/api/categories", json=category_data)
    assert response.status_code == 400


# ========== 标签API测试 ==========
@pytest.mark.api
async def test_list_tags(client: AsyncClient, test_tag):
    """测试获取标签列表"""
    response = await client.get("/api/tags")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert len(data["data"]["items"]) == 1
    assert data["data"]["items"][0]["name"] == "测试标签"


@pytest.mark.api
async def test_popular_tags(client: AsyncClient, test_article):
    """测试热门标签"""
    response = await client.get("/api/tags/popular")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert len(data["data"]["items"]) > 0
    # 应该有count字段
    assert "count" in data["data"]["items"][0]


# ========== 搜索测试 ==========
@pytest.mark.api
async def test_search_articles(client: AsyncClient, test_article):
    """测试搜索文章"""
    response = await client.get("/api/search?q=测试")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["total"] == 1
    assert data["data"]["keyword"] == "测试"


@pytest.mark.api
async def test_search_articles_short_keyword(client: AsyncClient):
    """测试搜索关键词太短"""
    response = await client.get("/api/search?q=a")
    assert response.status_code == 400


@pytest.mark.api
async def test_search_articles_no_results(client: AsyncClient):
    """测试搜索无结果"""
    response = await client.get("/api/search?q=不存在的关键词xyz123")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["total"] == 0


# ========== 统计测试 ==========
@pytest.mark.api
async def test_get_stats(client: AsyncClient, test_article):
    """测试获取统计数据"""
    response = await client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 0
    assert data["data"]["article_count"] == 1
    assert data["data"]["category_count"] == 1
    assert data["data"]["tag_count"] == 1
    assert "total_views" in data["data"]
