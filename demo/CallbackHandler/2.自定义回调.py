import os
import time
from typing import Any, Optional, Union
from uuid import UUID

import dotenv
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk, LLMResult
from langchain_core.runnables import RunnablePassthrough

dotenv.load_dotenv()

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StdOutCallbackHandler, BaseCallbackHandler


class LLMOpsCallbackHandler(BaseCallbackHandler):
    """自定义llm回调处理器"""

    def on_chat_model_start(
            self,
            serialized: dict[str, Any],
            messages: list[list[BaseMessage]],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[list[str]] = None,
            metadata: Optional[dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Any:
        print("聊天模型开始执行了")
        print("serialized:", serialized)
        print("messages:", messages)

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        print("token生成了")
        print("token:", token)

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        end_at: float = time.time()
        print("程序结束时间：", end_at)


if __name__ == '__main__':
    # 1 构建组件
    prompt = ChatPromptTemplate.from_template("{query}")

    # 2 创建大语言模型
    llm = ChatOpenAI(model_name="gpt-3.5-turbo",
                     openai_api_key=os.getenv("OPENAI_API_KEY"),
                     openai_api_base=os.getenv("OPENAI_API_URL")
                     )

    # 3 构建链
    chain = {"query": RunnablePassthrough()} | prompt | llm | StrOutputParser()

    # 3 调用链得到结果
    # content = chain.invoke( // invoke 不会生成新token
    resp = chain.stream(
        "你好你是？",
        config={"callbacks": [StdOutCallbackHandler(), LLMOpsCallbackHandler()]}
    )

    # print(content)
    for chunk in resp:
        pass
