import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

if __name__ == '__main__':
    # 1. 编排提示模版
    prompt = ChatPromptTemplate.from_template("{query}")

    # 2.创建大语言模型
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")
                     )

    # 3. 创建字符串输出解析器
    parser = StrOutputParser()

    # 4. 调用大语言模型生成结果并解析
    content = parser.invoke(llm.invoke(prompt.invoke({"query": "你好，你是？"})))

    print(content)
