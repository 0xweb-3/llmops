from langchain_core.prompts import ChatPromptTemplate

if __name__ == '__main__':
    system_chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是OpenAI开发的聊天机器人，请根据用户的提问进行回复，我叫{username}"),
    ])
    human_chat_prompt = ChatPromptTemplate.from_messages([
        ("human", "{query}")
    ])
    chat_prompt = system_chat_prompt + human_chat_prompt
    print(chat_prompt.invoke({
        "username": "by0xin",
        "query": "你好，你是？"
    }).to_messages())
