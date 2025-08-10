import dotenv
from langchain_huggingface import HuggingFaceEndpointEmbeddings

dotenv.load_dotenv()

if __name__ == '__main__':
    embeddings = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2")
    query_vector = embeddings.embed_query("买到假货，退货")

    print(query_vector)
    print(len(query_vector))
