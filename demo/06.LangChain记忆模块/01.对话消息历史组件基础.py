from langchain_core.chat_history import InMemoryChatMessageHistory


if __name__ == '__main__':
    chat_history= InMemoryChatMessageHistory()
    chat_history.add_user_message("这是一段用户的对话描述")
    chat_history.add_ai_message("这是一段AI生成的对话信息")
    print(chat_history)
    print(chat_history.messages)