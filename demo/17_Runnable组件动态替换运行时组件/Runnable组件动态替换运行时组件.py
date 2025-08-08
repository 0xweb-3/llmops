import os

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField
from langchain_community.chat_models.baidu_qianfan_endpoint import QianfanChatEndpoint

dotenv.load_dotenv()

if __name__ == '__main__':
    prompt = ChatPromptTemplate.from_template("{query}")
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL"),
                     ).configurable_alternatives(ConfigurableField(id="llm"), default_key="gpt-3.5-turbo",  gpt4=ChatOpenAI(model="gpt-4o"), wenxin=QianfanChatEndpoint(),
)
    chain = prompt | llm | StrOutputParser()
    content = chain.invoke({"query": "你是什么大语言模型"}, config={"configurable": {"llm": "gpt4"}})
    print(content)