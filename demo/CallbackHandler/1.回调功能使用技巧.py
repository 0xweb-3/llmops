import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

dotenv.load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StdOutCallbackHandler

if __name__ == '__main__':
    # 1 构建组件
    prompt = ChatPromptTemplate.from_template("{query}")

    # 2 创建大语言模型
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")
                     )

    # 3 构建链
    chain = {"query": RunnablePassthrough()} | prompt | llm | StrOutputParser()

    # 3 调用链得到结果
    content = chain.invoke("你好你是？",
                           config={"callbacks": [StdOutCallbackHandler()]}
                           )

    print(content)
