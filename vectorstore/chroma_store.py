import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from utils.config import CHROMA_DB_DIR
import os

def get_chroma_store():
    """Initialise et retourne le connecteur vers la base vectorielle ChromaDB."""
    if not os.path.exists(CHROMA_DB_DIR):
        os.makedirs(CHROMA_DB_DIR)
        
    db = chromadb.PersistentClient(path=CHROMA_DB_DIR)
    chroma_collection = db.get_or_create_collection("medical_knowledge")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    return vector_store
