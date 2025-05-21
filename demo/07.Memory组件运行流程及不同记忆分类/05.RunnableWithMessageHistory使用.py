import os

import dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store.keys():
        store[session_id] = FileChatMessageHistory(f"./chat_history{session_id}.txt")
    return store[session_id]


if __name__ == '__main__':
    # 1. 创建提示模版
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个强大的聊天机器人，能根据用户提供的上下文来回复用户的问题。"),
        MessagesPlaceholder("history"),
        ("human", "{query}")
    ])

    # 2. 创建大语言模型
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL"))

    # 3. 创建链应用
    chain = prompt | llm | StrOutputParser()

    # 包装链
    with_message_chain = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="query",
        history_messages_key="history"
    )

    while True:
        query = input("Human:")

        if query == '\q':
            exit(0)

        # 4. 运行链并传递配置信息
        response = with_message_chain.stream(
            {"query": query},
            config={"configurable": {
                "session_id": "xinbl"
            }}
        )
        print("AI:", flush=True, end="")

        for chunk in response:
            print(chunk, flush=True, end="")
        print("")
