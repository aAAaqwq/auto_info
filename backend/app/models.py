"""
数据库模型定义
文章、分类、标签、媒体...都写在这
"""
from sqlalchemy import String, Integer, Text, Boolean, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .database import Base


# 文章-标签多对多关联表
article_tag_table = Table(
    "article_tag",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Category(Base):
    """文章分类表"""
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)  # URL友好的标识
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    icon: Mapped[str | None] = mapped_column(String(100), nullable=True)  # 图标（可选）

    # 关联文章
    articles: Mapped[list["Article"]] = relationship(
        "Article", back_populates="category", lazy="selectin"
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Tag(Base):
    """文章标签表"""
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Media(Base):
    """媒体表（图片/视频）"""
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False)  # 'image' 或 'video'
    url: Mapped[str] = mapped_column(String(500), nullable=False)  # 媒体URL
    thumbnail_url: Mapped[str | None] = mapped_column(String(500), nullable=True)  # 视频缩略图
    caption: Mapped[str | None] = mapped_column(String(255), nullable=True)  # 说明文字
    order_index: Mapped[int] = mapped_column(Integer, default=0)  # 排序

    # 关联文章
    article: Mapped["Article"] = relationship("Article", back_populates="media_items")


class Article(Base):
    """文章表 - 核心表！"""
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)  # URL友好的标识
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)  # 摘要
    content: Mapped[str] = mapped_column(Text, nullable=False)  # Markdown内容

    # 封面图
    cover_image: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # 分类和标签
    category_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)
    category: Mapped["Category"] = relationship("Category", back_populates="articles", lazy="selectin")
    tags: Mapped[list["Tag"]] = relationship(
        "Tag", secondary=article_tag_table, backref="articles", lazy="selectin"
    )

    # 作者信息（API上传时提供）
    author_name: Mapped[str] = mapped_column(String(100), default="AI助手")
    author_avatar: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # 状态
    status: Mapped[str] = mapped_column(String(20), default="draft")  # 'draft' 或 'published'
    is_original: Mapped[bool] = mapped_column(Boolean, default=True)  # 是否原创

    # 统计
    views: Mapped[int] = mapped_column(Integer, default=0)

    # 时间
    published_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联媒体
    media_items: Mapped[list["Media"]] = relationship(
        "Media", back_populates="article", cascade="all, delete-orphan", lazy="selectin"
    )

    def to_dict(self) -> dict:
        """转成字典，API返回用"""
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "summary": self.summary,
            "content": self.content,
            "cover_image": self.cover_image,
            "category": {"id": self.category.id, "name": self.category.name, "slug": self.category.slug} if self.category else None,
            "tags": [{"id": t.id, "name": t.name, "slug": t.slug} for t in self.tags],
            "author_name": self.author_name,
            "author_avatar": self.author_avatar,
            "status": self.status,
            "is_original": self.is_original,
            "views": self.views,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "media_items": [{
                "id": m.id,
                "type": m.type,
                "url": m.url,
                "thumbnail_url": m.thumbnail_url,
                "caption": m.caption,
            } for m in self.media_items],
        }

    def to_list_dict(self) -> dict:
        """列表页用，不返回content等大字段"""
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "summary": self.summary,
            "cover_image": self.cover_image,
            "category": {"id": self.category.id, "name": self.category.name, "slug": self.category.slug} if self.category else None,
            "tags": [{"id": t.id, "name": t.name, "slug": t.slug} for t in self.tags],
            "author_name": self.author_name,
            "author_avatar": self.author_avatar,
            "views": self.views,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
