from langchain_community.document_loaders import WebBaseLoader

if __name__ == '__main__':
    loader = WebBaseLoader("https://imooc.com")
    documents = loader.load()

    print(documents)
    print(len(documents))
    print(documents[0].page_content)
