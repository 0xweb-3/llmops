import os
from typing import Literal  # 限定某个变量、函数参数或返回值只能是某几个固定的字面量值

from langchain_core.prompts import ChatPromptTemplate
import dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough

dotenv.load_dotenv()


class RouteQuery(BaseModel):
    """将用户查询映射到对应的数据源上"""
    datasource: Literal["python_docs", "js_docs", "golang_docs"] = Field(
        description="根据用户的问题，选择哪个数据源最相关以回答用户的问题"
    )


def choose_route(result: RouteQuery) -> str:
    if "python_docs" in result.datasource:
        return "chain in python_docs"
    elif "js_docs" in result.datasource:
        return "chain in js_docs"
    else:
        return "golang_docs"


if __name__ == '__main__':
    # 1.创建绑定结构化输出的大语言模型
    llm = ChatOpenAI(model_name="gpt-4o",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL"),
                     temperature=0
                     )
    structured_llm = llm.with_structured_output(RouteQuery)

    # 2.创建路由逻辑链
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个擅长将用户问题路由到适当的数据源的专家。\n请根据问题涉及的编程语言，将其路由到相关数据源"),
        ("human", "{question}")
    ])

    router = {"question": RunnablePassthrough()} | prompt | structured_llm | choose_route

    # 3.执行相应的提问，检查映射的路由
    question = """为什么下面的代码不工作了，请帮我检查下：

    from langchain_core.prompts import ChatPromptTemplate

    prompt = ChatPromptTemplate.from_messages(["human", "speak in {language}"])
    prompt.invoke("中文")"""

    # 4.选择不同的类型
    print(router.invoke(question))
