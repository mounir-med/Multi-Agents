from typing import TypedDict, Any
from langgraph.graph import StateGraph, END
from agents.retrieval_agent import run_retrieval_agent
from agents.analysis_agent import run_analysis_agent
from agents.report_agent import run_report_agent
from agents.validation_agent import run_validation_agent
from utils.logger import logger

# État partagé enrichi pour supporter les sorties structurées
class AgentState(TypedDict):
    question: str
    document_filter: str
    retrieved_context: str
    retrieved_passages: list[dict]
    analysis: Any  # Devient un dict (AnalysisResponse)
    report: Any    # Devient un dict (MedicalReport)
    validation_status: str
    audit_results: Any # Devient un dict (ValidationAudit)
    final_output: Any

def build_workflow():
    """Construit et compile le graphe LangGraph de l'orchestration multi-agents."""
    workflow = StateGraph(AgentState)
    
    # Ajout des noeuds (agents)
    workflow.add_node("retrieval_agent", run_retrieval_agent)
    workflow.add_node("analysis_agent", run_analysis_agent)
    workflow.add_node("report_agent", run_report_agent)
    workflow.add_node("validation_agent", run_validation_agent)
    
    # Définition du flux / orchestration
    workflow.set_entry_point("retrieval_agent")
    
    workflow.add_edge("retrieval_agent", "analysis_agent")
    workflow.add_edge("analysis_agent", "report_agent")
    workflow.add_edge("report_agent", "validation_agent")
    workflow.add_edge("validation_agent", END)
    
    return workflow.compile()

def process_question(question: str, document_filter: str = ""):
    """Point d'entrée pour traiter une question via le pipeline complet."""
    logger.info(f"Début de l'orchestration pour la question : '{question}'")
    app = build_workflow()
    
    # Initialisation de l'état partagé
    initial_state = {
        "question": question,
        "document_filter": document_filter or "",
        "retrieved_context": "",
        "retrieved_passages": [],
        "analysis": {},
        "report": {},
        "validation_status": "",
        "audit_results": {},
        "final_output": ""
    }
    
    # Exécution du graphe
    result = app.invoke(initial_state)
    logger.info("Orchestration multi-agents terminée.")
    return result
