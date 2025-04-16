# 应用配置的默认值
DEFAULT_CONFIG = {
    "WTF_CSRF_ENABLED": "False",

    # SQLALCHEMY数据库配置
    "SQLALCHEMY_DATABASE_URI=postgresql": "postgresql://postgres:postgres@127.0.0.1:5430/mytest?client_encoding=utf8",
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_POOL_RECYCLE": 3600,
    "SQLALCHEMY_ECHO": "True",

}
