import os
from llama_index.core import SimpleDirectoryReader
from rag.index_builder import build_index
from utils.config import DATA_DIR
from utils.logger import logger

def ingest_data(input_files: list[str] | None = None):
    """Lit les documents du dossier data et construit l'index ChromaDB."""
    if input_files:
        logger.info(f"Démarrage de l'ingestion ciblée ({len(input_files)} fichier(s))...")
    else:
        logger.info(f"Démarrage de l'ingestion depuis {DATA_DIR}...")
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        logger.warning(f"Le dossier {DATA_DIR} n'existait pas. Il vient d'être créé. Placez-y vos documents médicaux et relancez.")
        return
        
    try:
        if input_files:
            documents = SimpleDirectoryReader(input_files=input_files).load_data()
        else:
            documents = SimpleDirectoryReader(DATA_DIR).load_data()
        if not documents:
            logger.warning("Aucun document n'a été trouvé pour l'ingestion.")
            return
            
        logger.info(f"{len(documents)} document(s) chargé(s). Début de la vectorisation...")
        build_index(documents)
        logger.info("Ingestion terminée avec succès. Les vecteurs sont stockés dans ChromaDB.")
        
    except Exception as e:
        logger.error(f"Erreur lors de l'ingestion : {e}")

if __name__ == "__main__":
    ingest_data()
