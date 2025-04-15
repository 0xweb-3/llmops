import datetime

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate, MessagesPlaceholder  # 消息占位符
)

if __name__ == '__main__':
    # prompt = PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
    # print(prompt.format(subject="程序员"))  # 请讲一个关于程序员的冷笑话
    #
    # prompt_value = prompt.invoke({
    #     "subject": "喜剧演员"
    # })
    # print(prompt_value.to_string())  # 请讲一个关于喜剧演员的冷笑话
    # print(prompt_value.to_messages())  # [HumanMessage(content='请讲一个关于喜剧演员的冷笑话')]

    # 提示模版
    # chat_prompt = ChatPromptTemplate.from_messages([
    #     ("system", "你是OpenAI开发的聊天机器人，请根据用户的提问进行回复，当前的时间为：{now}"),
    #     MessagesPlaceholder("chat_history"),  # 消息占位符
    #     HumanMessagePromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
    # ])
    # chat_value = chat_prompt.invoke({
    #     "now": datetime.datetime.now(),
    #     "chat_history": [],  # 没有值需要给空
    #     "subject": "作家"
    # })
    # print(chat_value)

    # chat_value = chat_prompt.invoke({
    #     "now": datetime.datetime.now(),
    #     "chat_history": [
    #         ("human", "我叫xin")
    #     ],
    #     "subject": "作家"
    # })
    # print(chat_value.to_string())
    # print(chat_value.to_messages())

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", "你是OpenAI开发的聊天机器人，请根据用户的提问进行回复，当前的时间为：{now}"),
        MessagesPlaceholder("chat_history"),  # 消息占位符
        HumanMessagePromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
    ]).partial(now=datetime.datetime.now())

    from langchain_core.messages import AIMessage

    chat_value = chat_prompt.invoke({
        # "now": datetime.datetime.now(),
        "chat_history": [
            ("human", "我叫xin"),
            AIMessage("你好我是chatGPT，有什么可以帮到您的。"),
        ],
        "subject": "作家"
    })
    print(chat_value.to_string())
    print(chat_value.to_messages())
