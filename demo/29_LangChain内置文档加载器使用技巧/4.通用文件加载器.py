from langchain_community.document_loaders import UnstructuredFileLoader

if __name__ == '__main__':
    loader = UnstructuredFileLoader("./项目API资料.md")
    documents = loader.load()

    print(documents)
    print(len(documents))
    print(documents[0].metadata)
