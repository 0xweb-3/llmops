import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

if __name__ == '__main__':
    # 1. 编排prompt
    joke_prompt = ChatPromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
    poem_prompt = ChatPromptTemplate.from_template("请写一篇关于{subject}的七言绝句诗")

    # 2. 创建大语言模型
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")
                     )
    # 3. 创建输出解释器
    parser = StrOutputParser()

    # 4. 编排链
    joke_chain = joke_prompt | llm | parser
    poem_chain = poem_prompt | llm | parser

    # 5. 并行链
    # map_chain = RunnableParallel({
    #     "joke": joke_chain,
    #     "poem": poem_chain
    # })
    map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

    res = map_chain.invoke({"subject": "农民"})
    print(res)
