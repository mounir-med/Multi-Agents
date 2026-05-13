from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from utils.config import MODEL_NAME, OLLAMA_BASE_URL
from utils.logger import logger
from utils.schemas import MedicalReport

def run_report_agent(state: dict) -> dict:
    """Agent 3 : Génère un rapport médical structuré avec Pydantic."""
    logger.info("--- AGENT 3: REPORT (STRUCTURED) ---")
    analysis = state["analysis"]
    context = state.get("retrieved_context", "")

    if isinstance(analysis, str) and "Information non trouvée" in analysis:
        return {"report": "Information non trouvée dans les documents."}
    
    llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, temperature=0.1)
    structured_llm = llm.with_structured_output(MedicalReport)
    
    prompt = PromptTemplate(
        template="""Vous êtes un médecin expert rédigeant un rapport en FRANÇAIS.

SOURCES DISPONIBLES :
1. ANALYSE PRÉALABLE : {analysis}
2. CONTEXTE RAG : {context}

VOTRE MISSION :
Remplissez TOUS les champs du MedicalReport. 

RÈGLES CRITIQUES :
- LANGUE : RÉPONDEZ EXCLUSIVEMENT EN FRANÇAIS.
- RÉSUMÉ (summary) : Obligatoire. Faites une synthèse de 2 phrases maximum.
- SYMPTÔMES (symptoms) : Listez tous les symptômes mentionnés.
- ANALYSE (clinical_analysis) : Développez l'analyse médicale en français.

Ne laissez aucun champ vide. Si une information est absente, écrivez "Non mentionné".

Rapport Médical :""",
        input_variables=["analysis", "context"]
    )
    
    try:
        chain = prompt | structured_llm
        report_result = chain.invoke({"analysis": str(analysis), "context": context})
        logger.info("Génération du rapport médical terminée.")
        return {"report": report_result.dict() if hasattr(report_result, 'dict') else report_result}
    except Exception as e:
        logger.error(f"Erreur lors de la génération du rapport : {e}")
        return {"report": {"summary": "Erreur", "symptoms": [], "clinical_analysis": str(e), "recommendations": [], "citations": []}}
