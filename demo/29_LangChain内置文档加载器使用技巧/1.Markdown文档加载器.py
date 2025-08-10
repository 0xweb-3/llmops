from langchain_community.document_loaders import UnstructuredMarkdownLoader

if __name__ == '__main__':
    loader = UnstructuredMarkdownLoader("./项目API资料.md", mode="paged") # mode="elements"
    documents = loader.load()

    print(documents)
    print(len(documents))
    print(documents[0].metadata)
