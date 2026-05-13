from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from vectorstore.chroma_store import get_chroma_store
from utils.config import MODEL_NAME, OLLAMA_BASE_URL, EMBED_MODEL_NAME

def get_retriever():
    """Crée et retourne le retriever pour chercher dans ChromaDB."""
    vector_store = get_chroma_store()
    
    # Configuration d'Ollama pour le retriever
    Settings.llm = Ollama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, request_timeout=120.0)
    Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL_NAME, base_url=OLLAMA_BASE_URL)
    
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
    )
    return index.as_retriever(similarity_top_k=5)
