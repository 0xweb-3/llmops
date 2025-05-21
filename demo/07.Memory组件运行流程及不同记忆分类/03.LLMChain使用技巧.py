import os

import dotenv
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

if __name__ == '__main__':
    prompt = ChatPromptTemplate.from_template("请讲一个{subject}的笑话")

    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL"))

    chain = LLMChain(prompt=prompt, llm=llm)

    # print(chain("程序员"))
    # print(chain.run("程序员"))
    # print(chain.apply([{"subject": "程序员"}]))
    # print(chain.generate([{f"subject": "程序员"}]))
    # print(chain.predict(subject="程序员"))

    print(chain.invoke({"subject": "律师"}))
