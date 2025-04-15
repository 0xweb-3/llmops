import os
from datetime import datetime

import dotenv

dotenv.load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

if __name__ == '__main__':
    # 1.编排prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是OpenAI开发的聊天机器人，请回答用户的问题，现在的时间是{now}"),
        ("human", "{query}")]).partial(now=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # 2.创建大语言模型
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")
                     )

    response = llm.stream(prompt.invoke({"query": "什么是吉卜力风格？"}))

    for chunk in response:
        # print(chunk.content)
        print(chunk.content, flush=True, end="")
