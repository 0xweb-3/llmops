import os
from operator import itemgetter

import dotenv
import weaviate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey, Auth

dotenv.load_dotenv()


def format_qa_pair(question: str, answer: str) -> str:
    """格式化传递的问题+答案为单个字符串"""
    return f"Question: {question}\nAnswer: {answer}\n\n".strip()


if __name__ == '__main__':
    # 1. 定义分解问题的prompt
    decomposition_prompt = ChatPromptTemplate.from_template(
        "你是一个乐于助人的AI助理，可以针对一个输入问题生成多个相关的子问题。\n"
        "目标是将输入问题分解成一组可以独立回答的子问题或者子任务。\n"
        "生成与一下问题相关的多个搜索查询：{question}\n"
        "并使用换行符进行分割，输出（3个子问题/子查询）："
    )

    # 2.构建分解问题链
    decomposition_chain = (
            {"question": RunnablePassthrough()}
            | decomposition_prompt
            | ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_URL"), )
            | StrOutputParser()
            | (lambda x: x.strip().split("\n"))
    )

    # 3. 创建连接客户端
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=Auth.api_key(os.getenv("WEAVIATE_KEY")),
        skip_init_checks=True  # 跳过 gRPC + meta 检查
    )
    db = WeaviateVectorStore(
        client=client,
        index_name="tryData",
        text_key="text",
        embedding=OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_API_URL"))
    )
    retriever = db.as_retriever(search_type="mmr")

    # 4.执行提问获取子问题
    question = "关于笨笨信息有哪些"
    sub_questions = decomposition_chain.invoke(question)
    # print(sub_questions)

    # 5. 构建迭代问答链： 提示模版+链
    prompt = ChatPromptTemplate.from_template("""这是你需要回答的问题：
        ---
        {question}
        ---
        
        这是所有可用的背景问题和答案对：
        ---
        {qa_pairs}
        ---
        
        这是与问题相关的额外背景信息：
        ---
        {context}
        ---""")
    chain = (
            {
                "question": itemgetter("question"),
                "qa_pairs": itemgetter("qa_pairs"),
                "context": itemgetter("question") | retriever,
            }
            | prompt
            | ChatOpenAI(
        model="gpt-3.5-turbo-16k",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_URL"),
        temperature=0,
            )
            | StrOutputParser()
    )
    # 5.循环遍历所有子问题进行检索并获取答案
    qa_pairs = ""
    for sub_question in sub_questions:
        answer = chain.invoke({"question": sub_question, "qa_pairs": qa_pairs})
        qa_pair = format_qa_pair(sub_question, answer)
        qa_pairs += "\n---\n" + qa_pair
        print(f"问题: {sub_question}")
        print(f"答案: {answer}")
