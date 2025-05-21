import os

import dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

if __name__ == '__main__':
    # 1. 创建提示模版
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个强大的聊天机器人，能根据用户提供的上下文来回复用户的问题。\n\n <context>{context}</context>"),
        ("human", "{query}")
    ])

    # 2. 创建大语言模型
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL"))

    # 3. 创建链应用
    chain = create_stuff_documents_chain(prompt=prompt, llm=llm)

    # 4. 文档列表
    documents = [
        Document(page_content="小明喜欢绿色，但不喜欢黄色"),
        Document(page_content="小王喜欢粉色，但不喜欢红色"),
        Document(page_content="小新喜欢蓝色，但更喜欢绿色")
    ]

    # 5. 调用链
    context = chain.invoke({"query": "请帮我统计一下大家都喜欢什么颜色", "context": documents})
    print(context)
