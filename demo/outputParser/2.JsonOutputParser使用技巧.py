import os

import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field

dotenv.load_dotenv()

if __name__ == '__main__':
    # 1.创建一个json数据结构，用于告诉大语言模型这个json长什么样子
    class Joke(BaseModel):
        # 冷笑话
        joke: str = Field(description="回答用户的冷笑话")
        # 冷笑话的笑点
        punchline: str = Field(description="这个冷笑话的笑点")


    # 2. 创建字符串输出解析器
    parser = JsonOutputParser(pydantic_object=Joke)

    # 3. 构建一个提示模版
    prompt = (ChatPromptTemplate.from_template("请根据用户的提问进行回答。\n{format_instructions}\n{query}").
              partial(format_instructions=parser.get_format_instructions()))

    # print(prompt.format(query="请讲一个关于法官的冷笑话"))

    # 3.创建大语言模型
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")
                     )

    # 4. 调用大语言模型生成结果并解析
    content = parser.invoke(llm.invoke(prompt.invoke({"query": "请讲一个关于法官的冷笑话"})))

    print(content)
