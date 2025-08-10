from langchain_community.document_loaders import TextLoader

if __name__ == '__main__':
    # 1. 构建加载器
    loader = TextLoader("./电商产品数据.txt", encoding="utf-8")
    # 2. 加载数据
    document = loader.load()

    print(document)
    print(len(document))
    print(document[0].metadata)