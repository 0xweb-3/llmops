import os

import dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from openai import OpenAI

dotenv.load_dotenv()

if __name__ == '__main__':
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        base_url=os.getenv("OPENAI_API_URL"),
    )
    chat_history = FileChatMessageHistory(file_path="./chat_history.json")  # 记忆存储类

    while True:
        query = input("Human:")

        if query == '\q':
            break

        # 将历史消息写入后的系统提示词
        system_prompt = (
            "你是0penAI开发的ChatGPT聊天机器人,可以根据相应的上下文回复用户信息,上下文里存放的是人类与你对话的信息列表。\n\n",
            f"<context>{chat_history}</context>\n\n"
        )

        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": system_prompt},  # 将历史消息塞入
                {"role": "user", "content": query}
            ],
            stream=True)

        print("AI:", flush=True, end="")
        ai_content = ""
        for chunk in response:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            if hasattr(delta, 'content') and delta.content is not None:
                ai_content += delta.content
                print(delta.content, flush=True, end="")
        chat_history.add_user_message(query)
        chat_history.add_ai_message(ai_content)
        print("")
