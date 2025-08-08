import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField

dotenv.load_dotenv()


if __name__ == '__main__':
    # 1.创建提示模板
    prompt = PromptTemplate.from_template("请生成一个小于{x}的随机整数")

    # 2.创建LLM大语言模型，并配置temperature参数为可在运行时配置，配置键位llm_temperature
    llm = (ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")).
           configurable_fields(temperature=ConfigurableField(
        id="llm_temperature",
        name="大预言模型温度",
        description="温度越低，大预言模型生成内容越确定")))

    # 3.构建链应用
    chain = prompt | llm | StrOutputParser()

    # 4.正常调用内容
    content = chain.invoke({"x": 1000})
    print(content)

    print("==#==#==#==#==#==#")

    # 5.将temperature修改为0调用内容
    content = chain.invoke({"x": 1000}, config={"configurable": {"llm_temperature": 0}})
    print(content)
