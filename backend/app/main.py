"""
FastAPI主入口文件
老王给你搭好了，别tm乱改核心逻辑！
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import Optional, List
from datetime import datetime
import re
import uvicorn

from .config import settings
from .database import get_db, init_db, engine
from .models import Article, Category, Tag, Media
from .schemas import (
    ArticleListSchema,
    ArticleDetailSchema,
    ArticleCreateSchema,
    ArticleUpdateSchema,
    CategorySchema,
    CategoryCreateSchema,
    TagSchema,
    ApiResponse,
    PaginatedResponse,
)


# ========== 生命周期管理 ==========
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理 - 老王说优雅关闭很重要！
    启动时初始化，关闭时清理资源
    """
    # 启动时执行
    await init_db()
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} started successfully!")
    print(f"API docs: http://localhost:8000/api/docs")

    yield  # 应用运行期间

    # 关闭时执行 - 优雅关闭数据库连接
    print("Shutting down database connection...")
    await engine.dispose()
    print("Graceful shutdown completed!")


# 创建FastAPI应用（使用lifespan替代on_event）
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI智能资讯聚合系统 API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,  # 使用新的lifespan参数
)


# CORS中间件配置 - 前后端分离必须的！
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== 异常处理 ==========
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """统一处理HTTP异常"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "message": exc.detail, "data": None},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """处理其他所有异常"""
    import traceback

    print(f"艹，出错了：{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"code": 500, "message": str(exc) if settings.DEBUG else "服务器内部错误", "data": None},
    )


# ========== 辅助函数 ==========
def generate_slug(title: str) -> str:
    """生成URL友好的slug，老王我亲自写的！"""
    # 转小写，替换空格和特殊字符为连字符
    slug = re.sub(r"[^\w\s-]", "", title.lower())
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug.strip("-")


async def get_article_by_id_or_slug(db: AsyncSession, id_or_slug: str | int) -> Article | None:
    """通过ID或slug获取文章"""
    if isinstance(id_or_slug, int) or id_or_slug.isdigit():
        return await db.get(Article, int(id_or_slug))
    else:
        result = await db.execute(select(Article).where(Article.slug == id_or_slug))
        return result.scalar_one_or_none()


async def get_or_create_tags(db: AsyncSession, tag_names: List[str]) -> List[Tag]:
    """获取或创建标签，老王这个函数写得很优雅！"""
    tags = []
    for name in tag_names:
        if not name or not name.strip():
            continue
        name = name.strip()
        result = await db.execute(select(Tag).where(Tag.name == name))
        tag = result.scalar_one_or_none()
        if not tag:
            slug = generate_slug(name)
            # 确保slug唯一
            existing = await db.execute(select(Tag).where(Tag.slug == slug))
            if existing.scalar_one_or_none():
                slug = f"{slug}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            tag = Tag(name=name, slug=slug)
            db.add(tag)
            await db.flush()
        tags.append(tag)
    return tags


# ========== API路由 ==========

# 健康检查
@app.get("/", response_model=ApiResponse)
async def root():
    """根路径，健康检查用"""
    return ApiResponse(code=0, message=f"{settings.APP_NAME} is running", data={"version": settings.APP_VERSION})


@app.get("/api/health", response_model=ApiResponse)
async def health_check():
    """健康检查接口"""
    return ApiResponse(code=0, message="OK", data={"status": "healthy"})


# ========== 文章API ==========
@app.get("/api/articles", response_model=PaginatedResponse)
async def list_articles(
    page: int = 1,
    page_size: int = 20,
    category: Optional[str] = None,
    tag: Optional[str] = None,
    status: str = "published",
    db: AsyncSession = Depends(get_db),
):
    """
    获取文章列表

    - **page**: 页码（从1开始）
    - **page_size**: 每页数量
    - **category**: 分类slug筛选
    - **tag**: 标签slug筛选
    - **status**: 文章状态筛选
    """
    query = select(Article).where(Article.status == status)

    # 按分类筛选
    if category:
        query = query.join(Category).where(Category.slug == category)

    # 按标签筛选
    if tag:
        query = query.join(Article.tags).where(Tag.slug == tag)

    # 按发布时间倒序
    query = query.order_by(desc(Article.published_at), desc(Article.created_at))

    # 获取总数
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar() or 0

    # 分页
    total_pages = (total + page_size - 1) // page_size
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    articles = result.scalars().all()

    return PaginatedResponse(
        items=[article.to_list_dict() for article in articles],
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@app.get("/api/articles/{id_or_slug}", response_model=ApiResponse)
async def get_article(id_or_slug: str, db: AsyncSession = Depends(get_db)):
    """获取文章详情"""
    article = await get_article_by_id_or_slug(db, id_or_slug)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 增加浏览次数
    article.views += 1
    await db.commit()

    return ApiResponse(code=0, message="success", data=article.to_dict())


@app.post("/api/articles", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_article(article_data: ArticleCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    创建文章（API上传用）

    支持的内容格式：
    - content: HTML格式的正文（Quill编辑器输出）
    - media_items: 媒体列表 [{type:'image|video', url:'...', caption:'...'}]
    """
    # 生成slug（如果没提供）
    if not article_data.slug:
        slug = generate_slug(article_data.title)
        # 确保slug唯一
        counter = 1
        original_slug = slug
        while (await db.execute(select(Article).where(Article.slug == slug))).scalar_one_or_none():
            slug = f"{original_slug}-{counter}"
            counter += 1
    else:
        slug = article_data.slug

    # 检查slug是否已存在
    existing = await db.execute(select(Article).where(Article.slug == slug))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail=f"Slug '{slug}' 已存在")

    # 获取或创建分类
    category = None
    if article_data.category_id:
        category = await db.get(Category, article_data.category_id)
        if not category:
            raise HTTPException(status_code=400, detail="分类不存在")

    # 获取或创建标签
    tags = await get_or_create_tags(db, article_data.tags) if article_data.tags else []

    # 创建文章
    article = Article(
        title=article_data.title,
        slug=slug,
        summary=article_data.summary,
        content=article_data.content,
        cover_image=article_data.cover_image,
        category_id=article_data.category_id,
        author_name=article_data.author_name,
        author_avatar=article_data.author_avatar,
        is_original=article_data.is_original,
        status=article_data.status,
        published_at=article_data.published_at or datetime.utcnow(),
    )

    # 设置关联
    if category:
        article.category = category
    if tags:
        article.tags = tags

    db.add(article)
    await db.flush()  # 获取article.id

    # 添加媒体项
    if article_data.media_items:
        for media_item in article_data.media_items:
            media = Media(
                article_id=article.id,
                type=media_item.get("type", "image"),
                url=media_item.get("url", ""),
                thumbnail_url=media_item.get("thumbnail_url"),
                caption=media_item.get("caption"),
                order_index=media_item.get("order_index", 0),
            )
            db.add(media)

    await db.commit()
    await db.refresh(article)

    return ApiResponse(code=0, message="文章创建成功", data=article.to_dict())


@app.put("/api/articles/{article_id}", response_model=ApiResponse)
async def update_article(
    article_id: int,
    article_data: ArticleUpdateSchema,
    db: AsyncSession = Depends(get_db),
):
    """更新文章"""
    article = await db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 更新字段
    update_data = article_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "tags":
            # 特殊处理标签
            tags = await get_or_create_tags(db, value) if value else []
            article.tags = tags
        elif field == "category_id":
            # 验证分类存在
            if value:
                category = await db.get(Category, value)
                if not category:
                    raise HTTPException(status_code=400, detail="分类不存在")
            setattr(article, "category_id", value)
        elif field == "media_items":
            # 更新媒体项（删除旧的，添加新的）
            for old_media in article.media_items:
                await db.delete(old_media)
            for media_item in value:
                media = Media(
                    article_id=article.id,
                    type=media_item.get("type", "image"),
                    url=media_item.get("url", ""),
                    thumbnail_url=media_item.get("thumbnail_url"),
                    caption=media_item.get("caption"),
                    order_index=media_item.get("order_index", 0),
                )
                db.add(media)
        else:
            setattr(article, field, value)

    article.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(article)

    return ApiResponse(code=0, message="文章更新成功", data=article.to_dict())


@app.delete("/api/articles/{article_id}", response_model=ApiResponse)
async def delete_article(article_id: int, db: AsyncSession = Depends(get_db)):
    """删除文章"""
    article = await db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    await db.delete(article)
    await db.commit()

    return ApiResponse(code=0, message="文章删除成功")


# ========== 分类API ==========
@app.get("/api/categories", response_model=ApiResponse)
async def list_categories(db: AsyncSession = Depends(get_db)):
    """获取所有分类"""
    result = await db.execute(select(Category).order_by(Category.id))
    categories = result.scalars().all()

    return ApiResponse(
        code=0,
        message="success",
        data={
            "items": [
                {"id": c.id, "name": c.name, "slug": c.slug, "description": c.description, "icon": c.icon}
                for c in categories
            ]
        },
    )


@app.post("/api/categories", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category_data: CategoryCreateSchema, db: AsyncSession = Depends(get_db)):
    """创建分类"""
    # 检查名称是否重复
    existing = await db.execute(select(Category).where(Category.name == category_data.name))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="分类名称已存在")

    slug = category_data.slug or generate_slug(category_data.name)

    category = Category(
        name=category_data.name,
        slug=slug,
        description=category_data.description,
        icon=category_data.icon,
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)

    return ApiResponse(code=0, message="分类创建成功", data={"id": category.id, "name": category.name, "slug": category.slug})


# ========== 标签API ==========
@app.get("/api/tags", response_model=ApiResponse)
async def list_tags(db: AsyncSession = Depends(get_db)):
    """获取所有标签"""
    result = await db.execute(select(Tag).order_by(Tag.name))
    tags = result.scalars().all()

    return ApiResponse(
        code=0,
        message="success",
        data={"items": [{"id": t.id, "name": t.name, "slug": t.slug} for t in tags]},
    )


@app.get("/api/tags/popular", response_model=ApiResponse)
async def popular_tags(limit: int = 20, db: AsyncSession = Depends(get_db)):
    """获取热门标签（按文章数量排序）"""
    query = (
        select(Tag.id, Tag.name, Tag.slug, func.count(Article.id).label("article_count"))
        .join(Article.tags)
        .group_by(Tag.id)
        .order_by(desc("article_count"))
        .limit(limit)
    )

    result = await db.execute(query)
    tags = result.all()

    return ApiResponse(
        code=0,
        message="success",
        data={"items": [{"id": t.id, "name": t.name, "slug": t.slug, "count": t.article_count} for t in tags]},
    )


# ========== 搜索API ==========
@app.get("/api/search", response_model=ApiResponse)
async def search_articles(
    q: str,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """
    搜索文章

    - **q**: 搜索关键词（标题或内容）
    - **page**: 页码
    - **page_size**: 每页数量
    """
    if not q or len(q.strip()) < 2:
        raise HTTPException(status_code=400, detail="搜索关键词至少2个字符")

    keyword = f"%{q.strip()}%"
    query = select(Article).where(
        Article.status == "published",
        (Article.title.ilike(keyword)) | (Article.content.ilike(keyword)),
    )

    # 获取总数
    total_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = total_result.scalar() or 0

    # 分页
    total_pages = (total + page_size - 1) // page_size
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)
    articles = result.scalars().all()

    return ApiResponse(
        code=0,
        message="success",
        data={
            "items": [article.to_list_dict() for article in articles],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "keyword": q,
        },
    )


# ========== 统计API ==========
@app.get("/api/stats", response_model=ApiResponse)
async def get_stats(db: AsyncSession = Depends(get_db)):
    """获取网站统计数据"""
    # 文章总数
    article_count = await db.execute(select(func.count(Article.id)).where(Article.status == "published"))
    article_count = article_count.scalar() or 0

    # 分类数
    category_count = await db.execute(select(func.count(Category.id)))
    category_count = category_count.scalar() or 0

    # 标签数
    tag_count = await db.execute(select(func.count(Tag.id)))
    tag_count = tag_count.scalar() or 0

    # 总浏览量
    total_views = await db.execute(select(func.sum(Article.views)))
    total_views = total_views.scalar() or 0

    # 最新文章
    latest_result = await db.execute(
        select(Article)
        .where(Article.status == "published")
        .order_by(desc(Article.published_at))
        .limit(5)
    )
    latest_articles = latest_result.scalars().all()

    return ApiResponse(
        code=0,
        message="success",
        data={
            "article_count": article_count,
            "category_count": category_count,
            "tag_count": tag_count,
            "total_views": total_views,
            "latest_articles": [a.to_list_dict() for a in latest_articles],
        },
    )


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
