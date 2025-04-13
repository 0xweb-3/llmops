import os

from flask import Flask
from flask_migrate import Migrate

from config import Config
from internal.exception import CustomException
from internal.model import App
from internal.router import Router
from pkg.response import json, Response, HttpCode
from pkg.sqlalchemy import SQLAlchemy


class Http(Flask):
    """Http服务引擎"""

    def __init__(self,
                 *args,
                 conf: Config,
                 db: SQLAlchemy,
                 migrate: Migrate,
                 router: Router,

                 **kwargs):
        super().__init__(*args, **kwargs)
        # 通过类的方式将应用配置加载
        self.config.from_object(conf)

        # 绑定异常错误处理
        self.register_error_handler(Exception, self._register_error_handler)

        # 初始化SQLAlchemy扩展
        db.init_app(self)
        migrate.init_app(self, db, directory="internal/migration")
        # 创建数据库表
        with self.app_context():
            _ = App()  # 确保项目代码一定能检索到app模型
            db.create_all()

        # 注册应用路由
        router.register_router(self)

    def _register_error_handler(self, err: Exception):
        # 1.异常信息是不是我们的自定义异常，如果是可以提取message和code等信息
        if isinstance(err, CustomException):
            return json(Response(
                code=err.code,
                message=err.message,
                data=err.data if err.data is not None else {}
            ))
        # 2.如果不是我们的自定义异常，则有可能是程序
        if self.debug or os.getenv('FLASK_ENV') == "development":
            raise err
        else:
            return json(Response(
                code=HttpCode.FAIL,
                message=str(err),
                data={}
            ))
