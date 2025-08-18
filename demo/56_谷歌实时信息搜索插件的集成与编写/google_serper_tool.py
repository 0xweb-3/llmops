import os

import dotenv
from pydantic import BaseModel, Field
from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper

dotenv.load_dotenv()
print(os.getenv("SERPER_API_KEY"))

class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜索的查询语句")


if __name__ == '__main__':
    google_serper = GoogleSerperRun(
        name="google_serper",
        description=(
            "一个低成本的谷歌搜索API。"
            "当你需要回答有关时事的问题时，可以调用该工具。"
            "该工具传递的参数是搜索查询语句。"
        ),
        args_schema=GoogleSerperArgsSchema,
        api_wrapper=GoogleSerperAPIWrapper()
    )
    print(google_serper.invoke("什么是ccp"))
