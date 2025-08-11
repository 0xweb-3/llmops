from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader

if __name__ == '__main__':
    loader = FileSystemBlobLoader(".", show_progress=True)

    for blob in loader.yield_blobs():
        print(blob.as_string())
