import os
from operator import itemgetter

import dotenv
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

if __name__ == '__main__':
    # 1. 创建提示模版
    # 创建一个记忆
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是OpenAI开发的聊天机器人,请根据对应的上下文回复用户问题"),
        MessagesPlaceholder("history"),
        ("human", "{query}"),
    ])
    memory = ConversationBufferWindowMemory(
        k=2,
        return_messages=True,  # 返回消息列表信息
        input_key="query",  # 明确指定哪个是用户问题
        output_key="output",
    )

    # 2. 构建大语言模型
    # memory_variable = memory.load_memory_variables({})
    # RunnablePassthrough.assign(history=lambda x: memory_variable.get("history"))

    # memory_variable = memory.load_memory_variables({})
    # RunnablePassthrough.assign(
    #     # history=RunnableLambda(memory.load_memory_variables) | (lambda x: x.get("history"))
    #     history=RunnableLambda(memory.load_memory_variables) | itemgetter("history"),
    # )

    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")
                     )

    # 3. 创建链应用
    chain = RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history"),
    ) | prompt | llm | StrOutputParser()

    # 4. 死循环构建对话命令行
    while True:
        query = input("Human:")

        if query == '\q':
            exit(0)

        chain_input = {"query": query}

        response = chain.stream(chain_input)
        print("AI:", flush=True, end="")

        output = ""
        for chunk in response:
            output += chunk
            print(chunk, flush=True, end="")
        memory.save_context(chain_input, {"output": output})
        print("")
        print("history:", memory.load_memory_variables({}))
