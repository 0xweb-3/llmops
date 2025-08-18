from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain_core.utils.function_calling import convert_to_openai_tool

if __name__ == '__main__':
    search = DuckDuckGoSearchResults()

    print(search("现任美国总统是谁"))
    print("名字：", search.name)
    print("描述：", search.description)
    print("参数：", search.args)
    print("是否直接返回：", search.return_direct)

    # print(convert_to_openai_tool(search))