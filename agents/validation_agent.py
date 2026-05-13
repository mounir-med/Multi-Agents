from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from utils.config import MODEL_NAME, OLLAMA_BASE_URL
from utils.logger import logger
from utils.schemas import ValidationAudit

def run_validation_agent(state: dict) -> dict:
    """Agent 4 : Valide le rapport médical via un audit structuré."""
    logger.info("--- AGENT 4: VALIDATION (STRUCTURED) ---")
    report = state["report"]
    question = state["question"]
    context = state.get("retrieved_context", "")

    if not context or "Information non trouvée" in str(report):
        return {
            "final_output": "Information non trouvée dans les documents.",
            "validation_status": "Échec - Aucun contexte"
        }
    
    llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, temperature=0.0)
    structured_llm = llm.with_structured_output(ValidationAudit)
    
    prompt = PromptTemplate(
        template="""Vous êtes un auditeur qualité médical. Auditez le rapport suivant par rapport au contexte.
        
Règles strictes :
1) Pas d'hallucinations.
2) Citations vérifiables.
3) Réponse à la question initiale : {question}

Contexte :
{context}

Rapport à auditer :
{report}

Effectuez l'audit de qualité :""",
        input_variables=["report", "question", "context"]
    )

    try:
        chain = prompt | structured_llm
        audit = chain.invoke({"report": str(report), "question": question, "context": context})
        
        # On préserve l'objet si valide, sinon on renvoie un message d'erreur
        final_output = report if audit.is_valid else {
            "summary": "Rapport Invalidé",
            "clinical_analysis": f"L'audit a échoué. Raisons : {audit.corrections_needed}",
            "symptoms": [],
            "recommendations": ["Recommencer l'analyse avec plus de contexte"],
            "citations": []
        }
        
        return {
            "final_output": final_output,
            "validation_status": "Validé" if audit.is_valid else "Invalidé",
            "audit_results": audit.dict() if hasattr(audit, 'dict') else audit
        }
    except Exception as e:
        logger.error(f"Erreur lors de la validation : {e}")
        return {
            "final_output": str(report),
            "validation_status": f"Erreur Audit: {str(e)}"
        }
