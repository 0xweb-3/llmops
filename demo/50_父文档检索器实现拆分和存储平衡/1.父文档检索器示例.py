import os

import dotenv
from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import weaviate
from weaviate.auth import Auth
from langchain_weaviate import WeaviateVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.storage import LocalFileStore
from langchain.retrievers import ParentDocumentRetriever

dotenv.load_dotenv()

if __name__ == '__main__':
    # 1.创建加载器与文档列表，并加载文档
    loaders = [
        UnstructuredLoader("./电商产品数据.txt"),
        UnstructuredLoader("./项目API文档.md"),
    ]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    # 2. 创建文档分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    # 3.创建向量数据库与文档数据库
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=os.getenv("WEAVIATE_URL"),
        auth_credentials=Auth.api_key(os.getenv("WEAVIATE_KEY")),
        skip_init_checks=True  # 跳过 gRPC + meta 检查
    )
    vector_store = WeaviateVectorStore(
        client=client,
        index_name="ParentDocument",
        text_key="text",
        embedding=OpenAIEmbeddings(model="text-embedding-3-small",
                                   openai_api_key=os.getenv("OPENAI_API_KEY"),
                                   openai_api_base=os.getenv("OPENAI_API_URL")),
    )
    byte_store = LocalFileStore("./parent-document")

    # 4.创建父文档检索器
    retriever = ParentDocumentRetriever(
        vectorstore=vector_store,
        byte_store=byte_store,
        child_splitter=text_splitter,
    )

    # 5.添加文档
    # retriever.add_documents(docs, ids=None)

    # 6.检索并返回内容
    # search_docs = retriever.invoke("分享关于LLMOps的一些应用配置")

    search_docs = retriever.vectorstore.similarity_search("分享关于LLMOps的一些应用配置")
    print(search_docs)
    print(len(search_docs))
