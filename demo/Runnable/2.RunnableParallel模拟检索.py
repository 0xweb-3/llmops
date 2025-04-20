import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def retrieval(query: str) -> str:
    """一个模拟的检索器函数"""
    print("正在进行内容检索。。。。。。 ")
    return "by0xin"


if __name__ == '__main__':
    # 1. 编排prompt
    prompt = ChatPromptTemplate.from_template("""请根据用户的问题回答，可以参考对应的上下文进行生成。
    
    <context>
    {context}   
    </context> 
    
    用户提问的问题是：{query}""")

    # 2. 创建大语言模型
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")
                     )
    # 3. 创建输出解释器
    parser = StrOutputParser()

    # 4. 构建链
    from operator import itemgetter

    chain = {
                "context": lambda x: retrieval(x["query"]),
                "query": itemgetter("query"),
            } | prompt | llm | parser

    # 5.调用链
    content = chain.invoke({"query": "你好，我是谁？"})

    print(content)
