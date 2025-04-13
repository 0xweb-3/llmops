import os
import uuid
from dataclasses import dataclass

from flask import request
from injector import inject
from openai import OpenAI

from internal.schema.app_schema import CompletionRequest
from internal.service import AppService
from pkg.response.response import success_json, validate_error_json, success_message


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        """调用服务创建新的App记录"""
        app = self.app_service.create_app()
        return success_message(f"创建成功APP，APP的Id为{app.id}")

    def get_app(self, id: uuid.UUID):
        """获取APP信息"""
        app = self.app_service.get_app(id)
        return success_message(f"获取APP成功，APP的名称为{app.name}")

    def update_app(self, id: uuid.UUID):
        """修改App信息"""
        app = self.app_service.update_app(id)
        return success_message(f"修改APP成功，APP的新名称为{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message("删除成功")

    def ping(self):
        return {"data": "pong"}

    def completion(self):
        """聊天接口"""
        req = CompletionRequest()
        if not req.validate():
            return validate_error_json(req.errors)

        # 1.提取从接口中获取的输入
        query = request.json.get("query")
        # 2.构建OpenAI客户端，并发起请求
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_URL"))
        # 3.得到请求响应，然后将OpenAI的响应传递给前端
        # completion = client.responses.create(
        #     model="gpt-3.5-turbo",
        #     input=query
        # )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}]
        )

        return success_json(response.choices[0].message.content)
