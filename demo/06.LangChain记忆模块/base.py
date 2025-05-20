import os

import dotenv
from openai import OpenAI

dotenv.load_dotenv()

if __name__ == '__main__':
    # 1. 创建openai客户端
    client = OpenAI(
        api_key=os.getenv('OPENAI_API_KEY'),
        base_url=os.getenv("OPENAI_API_URL"),
    )

    # 2. 创建一个循环进行对话
    while True:
        # 3. 获取人类的输入
        query = input("Human:")

        # 4. 判断用户输入的为\q, 如果是则推出
        if query == '\q':
            break

        # 5. 否则向openai发起请求，获取AI的回答
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{"role": "user", "content": query}],
            stream=True)

        # 6. 循环读取流式响应的内容
        print("AI:", flush=True, end="")
        ai_content = ""
        for chunk in response:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            if hasattr(delta, 'content') and delta.content is not None:
                ai_content += delta.content
                print(delta.content, flush=True, end="")
        print("")
