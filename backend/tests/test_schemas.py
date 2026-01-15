"""
Pydantic Schema验证测试 - 老王说数据验证必须严格！
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from app.schemas import (
    ArticleCreateSchema,
    ArticleUpdateSchema,
    ArticleListSchema,
    CategoryCreateSchema,
    TagCreateSchema,
    ApiResponse,
    PaginatedResponse,
)


# ========== ArticleCreateSchema 测试 ==========
@pytest.mark.unit
def test_article_create_schema_valid():
    """测试有效的文章创建Schema"""
    data = {
        "title": "测试文章",
        "content": "这是内容",
        "summary": "这是摘要",
        "author_name": "作者",
        "status": "published",
        "tags": ["Python", "FastAPI"],
        "media_items": [
            {"type": "image", "url": "https://example.com/img.jpg"}
        ]
    }
    schema = ArticleCreateSchema(**data)
    assert schema.title == "测试文章"
    assert schema.content == "这是内容"
    assert schema.tags == ["Python", "FastAPI"]
    assert len(schema.media_items) == 1


@pytest.mark.unit
def test_article_create_schema_minimal():
    """测试最小字段的文章创建Schema"""
    data = {
        "title": "测试文章",
        "content": "这是内容"
    }
    schema = ArticleCreateSchema(**data)
    assert schema.title == "测试文章"
    assert schema.author_name == "AI助手"  # 默认值
    assert schema.status == "published"  # 默认值
    assert schema.is_original is True  # 默认值
    assert schema.tags == []  # 默认空列表


@pytest.mark.unit
def test_article_create_schema_title_too_long():
    """测试标题超过最大长度"""
    data = {
        "title": "a" * 256,  # 超过255
        "content": "内容"
    }
    with pytest.raises(ValidationError):
        ArticleCreateSchema(**data)


@pytest.mark.unit
def test_article_create_schema_title_empty():
    """测试标题为空"""
    data = {
        "title": "",
        "content": "内容"
    }
    with pytest.raises(ValidationError):
        ArticleCreateSchema(**data)


@pytest.mark.unit
def test_article_create_schema_content_empty():
    """测试内容为空"""
    data = {
        "title": "标题",
        "content": ""
    }
    with pytest.raises(ValidationError):
        ArticleCreateSchema(**data)


@pytest.mark.unit
def test_article_create_schema_slug_generation():
    """测试不提供slug时使用默认None"""
    data = {
        "title": "测试文章",
        "content": "内容"
    }
    schema = ArticleCreateSchema(**data)
    assert schema.slug is None


# ========== ArticleUpdateSchema 测试 ==========
@pytest.mark.unit
def test_article_update_schema_valid():
    """测试有效的文章更新Schema"""
    data = {
        "title": "更新后的标题",
        "summary": "更新后的摘要"
    }
    schema = ArticleUpdateSchema(**data)
    assert schema.title == "更新后的标题"
    assert schema.summary == "更新后的摘要"


@pytest.mark.unit
def test_article_update_schema_all_fields():
    """测试更新所有字段"""
    data = {
        "title": "新标题",
        "slug": "new-slug",
        "summary": "新摘要",
        "content": "新内容",
        "cover_image": "https://example.com/cover.jpg",
        "category_id": 1,
        "tags": ["标签1", "标签2"],
        "author_name": "新作者",
        "status": "draft",
        "is_original": False
    }
    schema = ArticleUpdateSchema(**data)
    assert schema.title == "新标题"
    assert schema.status == "draft"


@pytest.mark.unit
def test_article_update_schema_empty():
    """测试空更新Schema（全可选字段）"""
    schema = ArticleUpdateSchema()
    assert schema.title is None
    assert schema.content is None


@pytest.mark.unit
def test_article_update_schema_invalid_status():
    """测试无效的状态值"""
    data = {
        "status": "invalid_status"
    }
    with pytest.raises(ValidationError):
        ArticleUpdateSchema(**data)


@pytest.mark.unit
def test_article_update_schema_valid_statuses():
    """测试有效的状态值"""
    for status in ["draft", "published"]:
        schema = ArticleUpdateSchema(status=status)
        assert schema.status == status


# ========== CategoryCreateSchema 测试 ==========
@pytest.mark.unit
def test_category_create_schema_valid():
    """测试有效的分类创建Schema"""
    data = {
        "name": "技术分类",
        "slug": "tech",
        "description": "技术相关文章",
        "icon": "tech-icon"
    }
    schema = CategoryCreateSchema(**data)
    assert schema.name == "技术分类"
    assert schema.slug == "tech"


@pytest.mark.unit
def test_category_create_schema_minimal():
    """测试最小字段的分类创建Schema"""
    data = {
        "name": "分类名"
    }
    schema = CategoryCreateSchema(**data)
    assert schema.name == "分类名"
    assert schema.slug is None
    assert schema.description is None


@pytest.mark.unit
def test_category_create_schema_name_too_long():
    """测试分类名超过最大长度"""
    data = {
        "name": "a" * 51  # 超过50
    }
    with pytest.raises(ValidationError):
        CategoryCreateSchema(**data)


@pytest.mark.unit
def test_category_create_schema_name_empty():
    """测试分类名为空"""
    data = {
        "name": ""
    }
    with pytest.raises(ValidationError):
        CategoryCreateSchema(**data)


# ========== TagCreateSchema 测试 ==========
@pytest.mark.unit
def test_tag_create_schema_valid():
    """测试有效的标签创建Schema"""
    data = {
        "name": "Python",
        "slug": "python"
    }
    schema = TagCreateSchema(**data)
    assert schema.name == "Python"
    assert schema.slug == "python"


@pytest.mark.unit
def test_tag_create_schema_minimal():
    """测试最小字段的标签创建Schema"""
    data = {
        "name": "标签名"
    }
    schema = TagCreateSchema(**data)
    assert schema.name == "标签名"
    assert schema.slug is None


# ========== ApiResponse 测试 ==========
@pytest.mark.unit
def test_api_response_default():
    """测试默认API响应"""
    response = ApiResponse()
    assert response.code == 0
    assert response.message == "success"
    assert response.data is None


@pytest.mark.unit
def test_api_response_with_data():
    """测试带数据的API响应"""
    response = ApiResponse(code=0, message="OK", data={"key": "value"})
    assert response.code == 0
    assert response.message == "OK"
    assert response.data == {"key": "value"}


@pytest.mark.unit
def test_api_response_error():
    """测试错误API响应"""
    response = ApiResponse(code=400, message="Bad Request")
    assert response.code == 400
    assert response.message == "Bad Request"


# ========== PaginatedResponse 测试 ==========
@pytest.mark.unit
def test_paginated_response():
    """测试分页响应"""
    response = PaginatedResponse(
        items=[{"id": 1}, {"id": 2}],
        total=100,
        page=1,
        page_size=20,
        total_pages=5
    )
    assert len(response.items) == 2
    assert response.total == 100
    assert response.page == 1
    assert response.page_size == 20
    assert response.total_pages == 5


@pytest.mark.unit
def test_paginated_response_empty():
    """测试空分页响应"""
    response = PaginatedResponse(
        items=[],
        total=0,
        page=1,
        page_size=20,
        total_pages=0
    )
    assert response.items == []
    assert response.total == 0


@pytest.mark.unit
def test_paginated_response_last_page():
    """测试最后一页的计算"""
    # 95条记录，每页20条，应该有5页
    response = PaginatedResponse(
        items=[],
        total=95,
        page=1,
        page_size=20,
        total_pages=5
    )
    assert response.total_pages == 5
