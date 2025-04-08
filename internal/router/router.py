from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler import AppHandler


@inject
@dataclass
class Router:
    """路由"""
    app_handler: AppHandler

    # dataclasses就不用显示的声明
    # def __init__(self, app_handler: AppHandler):
    #     self.app_handler = app_handler

    def register_router(self, app: Flask):
        """注册路由"""
        # 1. 创建蓝图
        bp = Blueprint('llmops', __name__, url_prefix="")

        # 2. 将url与对应的控制器方法绑定
        # app_handler = AppHandler()
        bp.add_url_rule("/ping", methods=["GET", "POST"], view_func=self.app_handler.ping)
        bp.add_url_rule("/chat", methods=["POST"], view_func=self.app_handler.completion)
        # 3. 在应用上注册蓝图
        app.register_blueprint(bp)
