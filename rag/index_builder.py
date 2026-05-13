from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from utils.config import MODEL_NAME, OLLAMA_BASE_URL, EMBED_MODEL_NAME
from vectorstore.chroma_store import get_chroma_store
from utils.logger import logger
import os

def build_index(documents):
    """Construit ou met à jour l'index vectoriel à partir des documents."""
    logger.info("Initialisation de ChromaDB et des paramètres LlamaIndex...")
    vector_store = get_chroma_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Configuration globale pour utiliser Ollama (LLM + Embeddings rapides)
    Settings.llm = Ollama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, request_timeout=120.0)
    Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL_NAME, base_url=OLLAMA_BASE_URL)
    
    logger.info(f"Création de l'index vectoriel rapide avec le modèle {EMBED_MODEL_NAME}...")

    # Normalise et complète les métadonnées pour faciliter le filtrage (UI/API)
    try:
        for d in documents:
            md = getattr(d, "metadata", None) or {}
            file_path = md.get("file_path") or md.get("filepath") or md.get("path")
            if file_path:
                base = os.path.basename(str(file_path))
                md.setdefault("file_name", base)
                md.setdefault("source", base)
            d.metadata = md
    except Exception as e:
        logger.warning(f"Impossible d'enrichir les métadonnées des documents : {e}")

    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
    return index
