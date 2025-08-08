import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

if __name__ == '__main__':
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "你正在执行一项测试，请根据用户问题回答"
        ),
        (
            "human",
            "{query}"
        )
    ])
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL"),
                     )
    chain = prompt | llm.bind(model="gpt-4") | StrOutputParser()
    content = chain.invoke({"query": "当前使用的什么大语言模型"})
    print(content)
