from rag.retriever import get_retriever
from utils.logger import logger
from langchain_ollama import ChatOllama
from utils.config import MODEL_NAME, OLLAMA_BASE_URL
import os

def expand_query(query: str) -> list[str]:
    """Expanse la requête de manière concise. Désactivé pour les requêtes courtes (< 4 mots)."""
    words = query.split()
    if len(words) < 4:
        return [query]

    llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, temperature=0)
    # Prompt ultra-concis pour éviter le bavardage du LLM qui ralentit tout
    prompt = f"""Génère uniquement 2 variantes de recherche courtes pour : "{query}"
Réponds uniquement avec les variantes, une par ligne. Pas d'introduction."""
    
    try:
        # On limite le nombre de tokens pour aller plus vite
        response = llm.invoke(prompt)
        variations = [v.strip().strip('"').strip('- ') for v in response.content.split("\n") if v.strip() and len(v) > 3]
        return [query] + variations[:2]
    except Exception as e:
        logger.error(f"Erreur expansion rapide : {e}")
        return [query]

def run_retrieval_agent(state: dict) -> dict:
    """Agent 1 : Récupération intelligente du contexte avec expansion de requête."""
    logger.info("--- AGENT 1: RETRIEVAL (ADVANCED) ---")
    question = state["question"]
    document_filter = str(state.get("document_filter", "") or "").strip()

    # CAS IMAGE : Bypass du RAG textuel
    if document_filter.lower().endswith(('.jpg', '.png', '.jpeg')):
        return {
            "retrieved_context": f"[SOURCE_IMAGE: {document_filter}]",
            "retrieved_passages": [],
        }

    try:
        # 1. Expansion de la requête
        queries = expand_query(question)
        logger.info(f"Requêtes expansées : {queries}")

        retriever = get_retriever()
        all_nodes = []
        seen_texts = set()

        # 2. Récupération multi-requêtes
        for q in queries:
            nodes = retriever.retrieve(q)
            for n in nodes:
                if n.get_content() not in seen_texts:
                    all_nodes.append(n)
                    seen_texts.add(n.get_content())

        retrieved_passages = []
        for n in all_nodes:
            text = n.get_content()
            metadata = getattr(n, "metadata", None) or {}
            
            # Filtrage par document
            if document_filter:
                match = False
                f_low = document_filter.lower()
                for val in metadata.values():
                    if f_low in str(val).lower():
                        match = True
                        break
                if not match: continue

            retrieved_passages.append({"text": text, "metadata": dict(metadata)})

        context = "\n\n".join([p["text"] for p in retrieved_passages]).strip()
        
        if not context:
            logger.warning("Aucun contexte trouvé après expansion.")

        logger.info(f"Contexte récupéré : {len(retrieved_passages)} passage(s) unique(s).")
        
        return {
            "retrieved_context": context,
            "retrieved_passages": retrieved_passages,
        }
    except Exception as e:
        logger.error(f"Erreur Retrieval : {e}")
        return {"retrieved_context": "", "retrieved_passages": []}
