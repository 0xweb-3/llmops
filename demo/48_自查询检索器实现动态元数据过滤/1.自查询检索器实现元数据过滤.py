import os
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
import dotenv
from langchain_openai import OpenAIEmbeddings
from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers import SelfQueryRetriever  # 自查询检索器
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

if __name__ == '__main__':
    # 1. 构建文档数据并上传到向量数据库中
    documents = [
        Document(
            page_content="肖申克的救赎",
            metadata={"year": 1994, "rating": 9.7, "director": "弗兰克·德拉邦特"},
        ),
        Document(
            page_content="霸王别姬",
            metadata={"year": 1993, "rating": 9.6, "director": "陈凯歌"},
        ),
        Document(
            page_content="阿甘正传",
            metadata={"year": 1994, "rating": 9.5, "director": "罗伯特·泽米吉斯"},
        ),
        Document(
            page_content="泰坦尼克号",
            metadata={"year": 1997, "rating": 9.5, "director": "詹姆斯·卡梅隆"},
        ),
        Document(
            page_content="千与千寻",
            metadata={"year": 2001, "rating": 9.4, "director": "宫崎骏"},
        ),
        Document(
            page_content="星际穿越",
            metadata={"year": 2014, "rating": 9.4, "director": "克里斯托弗·诺兰"},
        ),
        Document(
            page_content="忠犬八公的故事",
            metadata={"year": 2009, "rating": 9.4, "director": "莱塞·霍尔斯道姆"},
        ),
        Document(
            page_content="三傻大闹宝莱坞",
            metadata={"year": 2009, "rating": 9.2, "director": "拉库马·希拉尼"},
        ),
        Document(
            page_content="疯狂动物城",
            metadata={"year": 2016, "rating": 9.2, "director": "拜伦·霍华德"},
        ),
        Document(
            page_content="无间道",
            metadata={"year": 2002, "rating": 9.3, "director": "刘伟强"},
        ),
    ]
    db = PineconeVectorStore(
        index_name="llmops",
        embedding=OpenAIEmbeddings(model="text-embedding-3-small",
                                   openai_api_key=os.getenv("OPENAI_API_KEY"),
                                   openai_api_base=os.getenv("OPENAI_API_URL")),
        namespace="dataset",
        text_key="text"
    )
    # retriever = db.as_retriever()
    db.add_documents(documents)

    # # 2. 创建自查询元数据
    # metadata_filed_infos = [  # 定义元数据过滤器的字段
    #     AttributeInfo(name="year", description="电影的年份", type="integer"),
    #     AttributeInfo(name="rating", description="电影的评分", type="float"),
    #     AttributeInfo(name="director", description="电影的导演", type="string"),
    # ]
    #
    # # 3. 创建子查询检索
    # self_query_retriever = SelfQueryRetriever.from_llm(
    #     llm=ChatOpenAI(model_name="gpt-4o",
    #                    openai_api_key=os.getenv("OPENAI_API_KEY"),
    #                    openai_api_base=os.getenv("OPENAI_API_URL"),
    #                    temperature=0),
    #     vectorstore=db,
    #     document_contents="电影的名字",
    #     metadata_field_info=metadata_filed_infos,
    #     enable_limit=True, )
    #
    # # 4. 检索示例
    # docs = self_query_retriever.invoke("查找下评分高于9.5分的电影")
    # print(docs)
    # print(len(docs))
    # print("===================")
    # base_docs = retriever.invoke("查找下评分高于9.5分的电影")
    # print(base_docs)
    # print(len(base_docs))

