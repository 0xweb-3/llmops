from typing import List

import dotenv
import weaviate
from langchain.load import dumps, loads
from langchain.retrievers import MultiQueryRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()

from typing import List
from json import dumps, loads  # 用于序列化和反序列化文档对象


def rrf(results: List[List], k: int = 60) -> List:
    """
    rrf算法，对传递的二层嵌套文档列表进行去重合并，并返回排名高的数据

    Args:
        results: List[List]，二层嵌套的文档列表，每个内层列表是一个排序好的文档集合
        k: int，参数k，默认60，用于计算RRF分数的分母

    Returns:
        List: 返回去重后的文档及对应得分，按得分降序排序
    """
    # 1.定义一个变量存储每个文档的得分信息，key为文档序列化字符串，value为得分
    fused_result = {}

    # 2.循环两层获取每一个文档信息
    for docs in results:
        # 该docs是一个有序文档列表，rank代表文档排名
        for rank, doc in enumerate(docs):
            # 3.使用dumps函数将类实例转换成字符串，作为唯一标识
            doc_str = dumps(doc)

            # 4.判断该文档字符串是否已经计算过得分，若没有则初始化
            if doc_str not in fused_result:
                fused_result[doc_str] = 0

            # 5.计算新的分数，rank从0开始，所以加1避免除0
            fused_result[doc_str] += 1 / (rank + k)

    # 6.执行排序操作，按得分降序排列，得到一个列表，元素为(反序列化后的文档对象, 得分)
    reranked_results = [
        (loads(doc_str), score)
        for doc_str, score in sorted(fused_result.items(), key=lambda x: x[1], reverse=True)
    ]

    return reranked_results


if __name__ == '__main__':
    # 1.构建向量数据库与检索器
    db = WeaviateVectorStore(
        client=weaviate.connect_to_wcs(
            cluster_url="https://mbakeruerziae6psyex7ng.c0.us-west3.gcp.weaviate.cloud",
            auth_credentials=AuthApiKey("ZltPVa9ZSOxUcfafelsggGyyH6tnTYQYJvBx"),
        ),
        index_name="DatasetDemo",
        text_key="text",
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
    )
    retriever = db.as_retriever(search_type="mmr")

    # 3.执行检索
    docs = retriever.invoke("关于LLMOps应用配置的文档有哪些")
    print(docs)
    print(len(docs))
