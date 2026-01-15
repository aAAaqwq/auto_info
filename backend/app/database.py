"""
数据库配置 - SQLAlchemy Async
老王用SQLite是因为简单，你要换MySQL/PostgreSQL自己改配置！
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings


# 创建异步引擎，SQLite用aiosqlite
engine = create_async_engine(
    settings.DATABASE_URL,
 echo=settings.DEBUG,  # 开发环境打印SQL，生产环境记得关掉！
)

# 创建Session工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 提交后不过期对象，这个很重要！
    autocommit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """所有ORM模型的基类，继承它就行"""
    pass


async def get_db() -> AsyncSession:
    """
    依赖注入用的数据库Session
    用法: db: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """初始化数据库表，启动时调用一次就行"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
