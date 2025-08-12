import os

import dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()


if __name__ == '__main__':
    # 1.构建加载器和文本分割器
    loader = UnstructuredFileLoader("./科幻短篇.txt")
    embedding = OpenAIEmbeddings(model="text-embedding-3-small",
                                 openai_api_key=os.getenv("OPENAI_API_KEY"),
                                 openai_api_base=os.getenv("OPENAI_API_URL"), )

    text_splitter = SemanticChunker(
        embeddings=embedding,
        number_of_chunks=10,
        add_start_index=True,
        sentence_split_regex=r"(?<=[。？！.?!])"  # 句子分割正则
    )

    # 2.加载文本与分割
    documents = loader.load()
    chunks = text_splitter.split_documents(documents)

    # 3.循环打印
    for chunk in chunks:
        print("独立块儿：", chunk.page_content)

        print("=====######")
        # print(f"块大小: {len(chunk.page_content)}, 元数据: {chunk.metadata}")
