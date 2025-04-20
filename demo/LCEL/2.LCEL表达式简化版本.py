import os

import dotenv
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

if __name__ == '__main__':
    # 1 构建组件
    prompt = ChatPromptTemplate.from_template("{query}")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")
                     )
    parser = StrOutputParser()

    # 2 创建链
    chain = prompt | llm | parser

    # 3 调用链得到结果
    print(chain.invoke({"query": "你可以绘制图片么"}))
