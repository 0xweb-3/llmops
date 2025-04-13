import os
from typing import Any

from config.default_config import DEFAULT_CONFIG


def _get_env(key: str) -> Any:
    """从环境变量中读取配置项，找不到就从默认中读取"""
    return os.getenv(key, DEFAULT_CONFIG.get(key))


def _get_bool_env(key: str) -> bool:
    """从环境变量中获取bool类型的配置"""
    value: str = _get_env(key)
    return value.lower() in ("True", "true")


class Config:
    def __init__(self):
        #  关闭wtf的csrf保护
        self.WTF_CSRF_ENABLED = _get_bool_env("WTF_CSRF_ENABLED")

        # 配置数据库配置
        self.SQLALCHEMY_DATABASE_URI = _get_env("SQLALCHEMY_DATABASE_URI")
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": int(_get_env("SQLALCHEMY_POOL_SIZE")),  # 连接池的大小
            "pool_recycle": int(_get_env("SQLALCHEMY_POOL_RECYCLE")),  # 每个连接的生命周期
        }
        self.WTF_CSRF_ENABLED = _get_bool_env("SQLALCHEMY_ECHO")  # 将sql语句执行打印
