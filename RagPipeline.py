from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader, UnstructuredMarkdownLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
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

    def file_loader(self, source):
    
        if source.endswith(".pdf"):
            loader = PyMuPDFLoader(source)
    
        elif source.endswith(".docx"):
            loader = Docx2txtLoader(source)
    
        elif source.endswith(".md"):
            loader = UnstructuredMarkdownLoader(source)
    
        elif source.endswith(".txt"):
            loader = TextLoader(source)
    
        else:
            raise ValueError("Unsupported source")
            
        self.document = loader.load()

    def text_splitting(self):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 100
        )

        self.chunks = text_splitter.split_documents(self.document)

    def document_retriever(self, question):
        retriever = self.vector_store.as_retriever(
            search_kwargs = {
                "k": 4
            }
        )

        result = retriever.invoke(question)
        return result