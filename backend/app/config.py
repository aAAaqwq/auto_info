"""
老王的配置文件 - 别tm乱改！
"""
from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    """应用配置类，别tm乱加没用的配置！"""

    # 基础配置
    APP_NAME: str = "Auto Info API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = "sqlite+aiosqlite:///./auto_info.db"

    # CORS配置 - 允许的前端地址
    CORS_ORIGINS: str = '["http://localhost:5173","http://localhost:3000"]'

    # API密钥
    API_KEY: str = "your-secret-api-key-change-this"

    @property
    def cors_origins_list(self) -> List[str]:
        """把CORS配置从字符串转成列表，这个SB pydantic必须这么搞"""
        try:
            return json.loads(self.CORS_ORIGINS)
        except:
            return ["http://localhost:5173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例，别tm到处new对象！
settings = Settings()
