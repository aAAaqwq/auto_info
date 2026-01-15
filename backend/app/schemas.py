"""
Pydantic Schemas - API请求/响应的数据结构定义
这个很重要，API文档自动生成靠它！
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime


# ========== 基础Schema ==========
class CategorySchema(BaseModel):
    """分类Schema"""
    id: int
    name: str
    slug: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class TagSchema(BaseModel):
    """标签Schema"""
    id: int
    name: str
    slug: str

    class Config:
        from_attributes = True


class MediaSchema(BaseModel):
    """媒体Schema"""
    id: int
    type: str = Field(..., description="媒体类型: image 或 video")
    url: str
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    order_index: int = 0

    class Config:
        from_attributes = True


# ========== 文章Schema ==========
class ArticleListSchema(BaseModel):
    """文章列表Schema（不包含content）"""
    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    category: Optional[CategorySchema] = None
    tags: List[TagSchema] = []
    author_name: str
    author_avatar: Optional[str] = None
    views: int = 0
    published_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ArticleDetailSchema(ArticleListSchema):
    """文章详情Schema（包含content和media）"""
    content: str
    media_items: List[MediaSchema] = []

    class Config:
        from_attributes = True


class ArticleCreateSchema(BaseModel):
    """创建文章的Schema（API上传用）"""
    title: str = Field(..., min_length=1, max_length=255, description="文章标题")
    slug: Optional[str] = Field(None, max_length=255, description="URL标识，不填则自动生成")
    summary: Optional[str] = Field(None, description="摘要")
    content: str = Field(..., min_length=1, description="HTML正文内容（Quill格式）")
    cover_image: Optional[str] = Field(None, description="封面图URL")
    category_id: Optional[int] = Field(None, description="分类ID")
    tags: List[str] = Field(default_factory=list, description="标签名称列表")
    author_name: str = Field("AI助手", max_length=100, description="作者名称")
    author_avatar: Optional[str] = Field(None, description="作者头像URL")
    is_original: bool = Field(True, description="是否原创")
    status: str = Field("published", description="状态: draft 或 published")

    # 媒体项（图片/视频）
    media_items: List[dict] = Field(
        default_factory=list,
        description="媒体列表: [{type:'image|video', url:'...', caption:'...'}]"
    )

    published_at: Optional[datetime] = Field(None, description="发布时间，不填则用当前时间")


class ArticleUpdateSchema(BaseModel):
    """更新文章的Schema"""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    summary: Optional[str] = None
    content: Optional[str] = Field(None, min_length=1)
    cover_image: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None
    author_name: Optional[str] = Field(None, max_length=100)
    author_avatar: Optional[str] = None
    is_original: Optional[bool] = None
    status: Optional[str] = Field(None, pattern="^(draft|published)$")
    published_at: Optional[datetime] = None
    media_items: Optional[List[dict]] = None


# ========== 分页Schema ==========
class PaginatedResponse(BaseModel):
    """分页响应Schema"""
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int


# ========== API响应Schema ==========
class ApiResponse(BaseModel):
    """统一API响应格式"""
    code: int = 0
    message: str = "success"
    data: Optional[dict] = None


# ========== 分类Schema ==========
class CategoryCreateSchema(BaseModel):
    """创建分类"""
    name: str = Field(..., min_length=1, max_length=50)
    slug: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=100)


class CategoryUpdateSchema(BaseModel):
    """更新分类"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    slug: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=100)


# ========== 标签Schema ==========
class TagCreateSchema(BaseModel):
    """创建标签"""
    name: str = Field(..., min_length=1, max_length=50)
    slug: Optional[str] = Field(None, max_length=50)


# ========== 简化文章Schema（用于搜索结果）==========
class ArticleSimpleSchema(BaseModel):
    """简化文章Schema（用于搜索建议、相关推荐）"""
    id: int
    title: str
    slug: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None

    class Config:
        from_attributes = True


# ========== 相关推荐响应Schema ==========
class RelatedArticlesResponse(BaseModel):
    """相关推荐响应"""
    by_tag: List[ArticleListSchema]
    by_category: List[ArticleListSchema]
