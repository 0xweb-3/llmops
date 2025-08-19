import os

import dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


@tool
def complex_tool(int_arg: int, float_arg: float, dict_arg: dict) -> int:
    """使用复杂工具进行复杂计算操作"""
    return int_arg * float_arg


if __name__ == '__main__':
    # 1.创建大语言模型并绑定工具
    llm = ChatOpenAI(model="gpt-3.5-turbo-16k").bind_tools([complex_tool], openai_api_key=os.getenv("OPENAI_API_KEY"),
                                                           openai_api_base=os.getenv("OPENAI_API_URL"))
    better_llm = ChatOpenAI(model="gpt-4o", openai_api_key=os.getenv("OPENAI_API_KEY"),
                            openai_api_base=os.getenv("OPENAI_API_URL")).bind_tools([complex_tool])

    # 2.创建链并执行工具
    better_chain = (better_llm | (lambda msg: msg.tool_calls[0]["args"]) | complex_tool)
    chain = (llm | (lambda msg: msg.tool_calls[0]["args"]) | complex_tool).with_fallbacks([better_chain])

    # 3.调用链
    print(chain.invoke("使用复杂工具，对应参数为5和2.1，不要忘记了dict_arg参数"))
