from langchain_huggingface import HuggingFaceEmbeddings

if __name__ == '__main__':
    embeddings = HuggingFaceEmbeddings(
        model_name="nomic-ai/nomic-embed-text-v1.5",
        cache_folder="./embeddings",
        model_kwargs={"trust_remote_code": True}
    )
    query_vector = embeddings.embed_query("买到假货，退货")

    print(query_vector)
    print(len(query_vector))
