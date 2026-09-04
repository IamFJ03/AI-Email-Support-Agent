from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
Document_store = BASE_DIR / 'Document_Store'

class RagRetriever:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name = "sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vector_store = Chroma(
            persist_directory= Document_store,
            embedding_function= self.embedding_model,
            collection_name= 'store'
        )

    def data_exists(self):
        result = self.vector_store._collection.get()

        return len(result["ids"])

    