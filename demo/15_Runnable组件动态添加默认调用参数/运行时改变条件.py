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
            "你正在执行一项测试，请重复用户传递的内容，除了重复其他均不要操作练"
        ),
        (
            "human",
            "{query}"
        )
    ])
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL"),
                     # stop=["world"]
                     )
    chain = prompt | llm.bind(stop="world") | StrOutputParser()
    content = chain.invoke({"query": "Hello world"})
    print(content)