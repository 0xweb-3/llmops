# 将文档切割为不超过500字符，并且每块之间文本重叠50个字符

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import CharacterTextSplitter

if __name__ == '__main__':
    # 1. 加载对应的文档
    loader = UnstructuredMarkdownLoader("./项目API文档.md")
    documents = loader.load()

    # 2. 创建文本分割器
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=500,
        chunk_overlap=50,
        add_start_index=True,
    )

    # 3. 分割文本
    chunks = text_splitter.split_documents(documents)

    for chunk in chunks:
        print(f"块大小:{len(chunk.page_content)}, 元数据:{chunk.metadata}")

    print(len(chunks))