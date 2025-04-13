import uuid
from dataclasses import dataclass

from injector import inject

from internal.model import App
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class AppService:
    """应用服务逻辑"""
    db: SQLAlchemy

    def create_app(self) -> App:
        """创建APP"""
        with self.db.auto_commit():
            # 1. 创建模型类实体
            app = App(name="测试机器人", account_id=uuid.uuid4(), icon="", description="这是一个测试用的机器人")
            # 2. 将实体类添加到session中
            self.db.session.add(app)
            # 3. 提交session会话
            # self.db.session.commit()
        return app

    def get_app(self, id: uuid.UUID) -> App:
        """获取app信息"""
        app = self.db.session.query(App).get(id)
        return app

    def update_app(self, id: uuid.UUID) -> App:
        with self.db.auto_commit():
            app = self.get_app(id)
            app.name = "一个新的机器人"
            # self.db.session.commit()
        return app

    def delete_app(self, id: uuid.UUID):
        with self.db.auto_commit():
            app = self.get_app(id)
            self.db.session.delete(app)
        # self.db.session.commit()
