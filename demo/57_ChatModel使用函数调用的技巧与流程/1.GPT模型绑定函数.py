import json
import os
from typing import Type, Any

import dotenv
import requests
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


class GaodeWeatherArgsSchema(BaseModel):
    city: str = Field(description="需要查询天气预报的目标城市，例如：广州")


class GaodeWeatherTool(BaseTool):
    """根据传入的城市名查询天气"""
    name: str = "gaode_weather"
    description: str = "当你想查询天气或者与天气相关的问题时可以使用的工具"  # 这里给大预言模型使用
    args_schema: Type[BaseModel] = GaodeWeatherArgsSchema  # 指定参数类型

    def _run(self, *args: Any, **kwargs: Any) -> str:
        """根据传入的城市名称运行调用api获取城市对应的天气预报信息"""
        # 1.获取高德API秘钥，如果没有创建的话，则抛出错误
        gaode_api_key = os.getenv("GAODE_API_KEY")
        if not gaode_api_key:
            return f"高德开放平台API未配置"

        # 2.从参数中获取city城市名字
        city = kwargs.get("city", "")
        api_domain = "https://restapi.amap.com/v3"
        session = requests.session()

        # 3.发起行政区域编码查询，根据city获取ad_code
        city_response = session.request(
            method="GET",
            url=f"{api_domain}/config/district?key={gaode_api_key}&keywords={city}&subdistrict=0",
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        city_response.raise_for_status()
        city_data = city_response.json()

        if city_data.get("info") == "OK":
            ad_code = city_data["districts"][0]["adcode"]

            # 4.根据得到的ad_code调用天气预报API接口，获取天气信息
            weather_response = session.request(
                method="GET",
                url=f"{api_domain}/weather/weatherInfo?key={gaode_api_key}&city={ad_code}&extensions=all",
                headers={"Content-Type": "application/json; charset=utf-8"},
            )
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            if weather_data.get("info") == "OK":
                # 5.返回最后的结果字符串
                return json.dumps(weather_data)
        return f"获取{city}天气预报信息失败"


if __name__ == '__main__':
    # 1.定义工具列表
    gaode_weather = GaodeWeatherTool()

    tool_dict = {
        gaode_weather.name: gaode_weather,
    }
    tools = [tool for tool in tool_dict.values()]

    # 2.创建Prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "你是由OpenAI开发的聊天机器人，可以帮助用户回答问题，必要时刻请调用工具帮助用户解答，如果问题需要多个工具回答，请一次性调用所有工具，不要分步调用"
        ),
        ("human", "{query}"),
    ])

    # 3.创建大语言模型并绑定工具
    llm = ChatOpenAI(model="gpt-4o",
                     temperature=0,
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL"))
    llm_with_tool = llm.bind_tools(tools=tools)

    # 4.创建链应用
    chain = {"query": RunnablePassthrough()} | prompt | llm_with_tool

    # 5.调用链应用，并获取输出响应
    query = "武汉现在天气怎样,有什么适合穿的衣服呢？"
    resp = chain.invoke(query)
    tool_calls = resp.tool_calls

    # 6.判断是工具调用还是正常输出结果
    if len(tool_calls) <= 0:
        print("生成内容: ", resp.content)
    else:
        # 7.将历史的系统消息、人类消息、AI消息组合
        messages = prompt.invoke(query).to_messages()
        messages.append(resp)

        # 8.循环遍历所有工具调用信息
        for tool_call in tool_calls:
            tool = tool_dict.get(tool_call.get("name"))  # 获取需要执行的工具
            print("正在执行工具: ", tool.name)
            content = tool.invoke(tool_call.get("args"))  # 工具执行的内容/结果
            print("工具返回结果: ", content)
            tool_call_id = tool_call.get("id")
            messages.append(ToolMessage(
                content=content,
                tool_call_id=tool_call_id,
            ))
        print("输出内容: ", llm.invoke(messages).content)
