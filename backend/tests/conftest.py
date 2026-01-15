"""
pytest配置和测试夹具
老王说：写测试就像喝酒，准备工作必须到位！
"""
import asyncio
import pytest
import tempfile
import os
from pathlib import Path
from typing import AsyncGenerator, Generator
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models import Base, Article, Category, Tag, Media
from app.database import get_db


# ========== 测试数据库配置 ==========
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """创建事件循环，异步测试必须的！"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db_engine():
    """
    创建内存数据库引擎用于测试
    每个测试函数都使用独立的数据库，互不干扰！
    """
    # 创建临时数据库文件
    temp_db = tempfile.NamedTemporaryFile(mode="w", suffix=".db", delete=False)
    temp_db.close()

    test_db_url = f"sqlite+aiosqlite:///{temp_db.name}"

    # 创建引擎
    engine = create_async_engine(
        test_db_url,
        echo=False,  # 测试时不打印SQL
    )

    # 创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # 清理
    await engine.dispose()
    os.unlink(temp_db.name)


@pytest.fixture(scope="function")
async def db_session(test_db_engine) -> AsyncGenerator[AsyncSession, None]:
    """
    创建数据库Session用于测试
    每个测试结束后自动回滚，保持测试隔离！
    """
    async_session_maker = async_sessionmaker(
        test_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with async_session_maker() as session:
        yield session
        # 测试结束回滚所有更改
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    创建测试客户端
    替换数据库依赖为测试数据库！
    """
    async def override_get_db():
        yield db_session

    # 替换数据库依赖
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    # 清理依赖覆盖
    app.dependency_overrides.clear()


# ========== 测试数据工厂 ==========
@pytest.fixture
async def test_category(db_session: AsyncSession) -> Category:
    """创建测试分类"""
    category = Category(
        name="测试分类",
        slug="test-category",
        description="这是测试用的分类",
        icon="test-icon"
    )
    db_session.add(category)
    await db_session.commit()
    await db_session.refresh(category)
    return category


@pytest.fixture
async def test_tag(db_session: AsyncSession) -> Tag:
    """创建测试标签"""
    tag = Tag(
        name="测试标签",
        slug="test-tag"
    )
    db_session.add(tag)
    await db_session.commit()
    await db_session.refresh(tag)
    return tag


@pytest.fixture
async def test_article(db_session: AsyncSession, test_category: Category, test_tag: Tag) -> Article:
    """创建测试文章（带分类和标签）"""
    article = Article(
        title="测试文章标题",
        slug="test-article",
        summary="这是测试文章的摘要",
        content="# 测试内容\n\n这是测试文章的正文内容。",
        cover_image="https://example.com/cover.jpg",
        author_name="测试作者",
        status="published",
        published_at=datetime.utcnow(),
    )
    article.category = test_category
    article.tags = [test_tag]

    db_session.add(article)
    await db_session.commit()
    await db_session.refresh(article)
    return article


@pytest.fixture
async def test_articles_batch(db_session: AsyncSession, test_category: Category) -> list[Article]:
    """创建一批测试文章，用于分页测试"""
    articles = []
    for i in range(25):  # 创建25篇文章，测试分页
        article = Article(
            title=f"测试文章 {i+1}",
            slug=f"test-article-{i+1}",
            summary=f"这是第{i+1}篇测试文章的摘要",
            content=f"# 第{i+1}篇测试文章\n\n内容...",
            author_name="测试作者",
            status="published",
            published_at=datetime.utcnow(),
        )
        article.category = test_category
        articles.append(article)
        db_session.add(article)

    await db_session.commit()
    return articles


@pytest.fixture
async def test_media(db_session: AsyncSession, test_article: Article) -> Media:
    """创建测试媒体项"""
    media = Media(
        article_id=test_article.id,
        type="image",
        url="https://example.com/image.jpg",
        thumbnail_url="https://example.com/thumb.jpg",
        caption="测试图片说明",
        order_index=0
    )
    db_session.add(media)
    await db_session.commit()
    await db_session.refresh(media)
    return media


# ========== 工具函数 ==========
def assert_valid_response(response, expected_code: int = 0):
    """断言API响应格式正确"""
    assert "code" in response.json()
    assert "message" in response.json()
    assert response.json()["code"] == expected_code


def assert_article_shape(data: dict):
    """断言文章数据结构正确"""
    required_fields = ["id", "title", "slug", "content", "author_name", "status"]
    for field in required_fields:
        assert field in data, f"缺少字段: {field}"
