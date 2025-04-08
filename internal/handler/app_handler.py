import os

from flask import request
from openai import OpenAI

from internal.schema.app_schema import CompletionRequest


class AppHandler:
    """应用控制器"""

    def ping(self):
        return {"data": "pong"}

    def completion(self):
        """聊天接口"""
        req = CompletionRequest()
        if not req.validate():
            return {"data": req.errors}

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
        return response.choices[0].message.content
