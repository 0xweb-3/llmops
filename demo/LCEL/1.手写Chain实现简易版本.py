import os
from typing import Any

import dotenv
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


# 2. 定义一个链
class Chain:
    steps: list = []

    def __init__(self, steps: list):
        self.steps = steps

    def invoke(self, input: Any) -> Any:
        for step in self.steps:
            input = step.invoke(input)
            print("步骤：", step)
            print("输出：", input)

            print("========")
        return input


if __name__ == '__main__':
    # 1 构建组件
    prompt = ChatPromptTemplate.from_template("{query}")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")
                     )
    parser = StrOutputParser()

    # 3 编排链
    chain = Chain([prompt, llm, parser])

    # 4. 执行链 并输出结果
    print(chain.invoke({"query": "你好，你是？"}))
