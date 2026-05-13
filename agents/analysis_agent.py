import base64
import os
import json
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from utils.config import MODEL_NAME, OLLAMA_BASE_URL, DATA_DIR
from utils.logger import logger
from utils.schemas import AnalysisResponse
from utils.tools import MEDICAL_TOOLS

def run_analysis_agent(state: dict) -> dict:
    """Agent 2 : Analyse médicale avec sortie structurée et outils."""
    logger.info("--- AGENT 2: ANALYSIS (STRUCTURED + TOOLS) ---")
    question = state["question"]
    context = state["retrieved_context"]
    doc_filter = state.get("document_filter", "")

    # Détection automatique de besoin d'outils (logique simplifiée)
    tool_results = ""
    q_low = question.lower()
    if "imc" in q_low or "bmi" in q_low or "poids" in q_low:
        # Tentative d'extraction de poids/taille simple ou via LLM
        # Pour cet exemple, on simule l'appel si les mots clés sont là
        logger.info("Détection d'un besoin de calcul IMC.")
        # Ici on pourrait appeler un LLM pour extraire les params, puis appeler l'outil
        # On va juste noter que l'outil est disponible
        tool_results += "\n[OUTIL DISPONIBLE: calculate_bmi]"

    if "interaction" in q_low or "médicament" in q_low:
        logger.info("Détection d'un besoin de vérification d'interactions.")
        tool_results += "\n[OUTIL DISPONIBLE: drug_interaction_check]"

    is_image = doc_filter.lower().endswith(('.jpg', '.png', '.jpeg'))
    
    try:
        if is_image:
            image_path = os.path.join(DATA_DIR, doc_filter)
            if os.path.exists(image_path):
                logger.info(f"Analyse visuelle de l'image : {doc_filter}")
                with open(image_path, "rb") as f:
                    img_base64 = base64.b64encode(f.read()).decode("utf-8")
                
                llm = ChatOllama(model="llava", base_url=OLLAMA_BASE_URL)
                message = HumanMessage(
                    content=[
                        {"type": "text", "text": f"""Analyse médicale visuelle. 
                        Question : {question}
                        Décrivez précisément ce que vous voyez : signes cliniques, lésions, matériel médical, ou contexte de la consultation. 
                        Soyez factuel et détaillé pour qu'un médecin puisse utiliser votre description."""},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                    ]
                )
                response = llm.invoke([message])
                return {"analysis": response.content}
        
        if not str(context or "").strip():
            return {"analysis": "Information non trouvée dans les documents."}
            
        llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, temperature=0.2)
        structured_llm = llm.with_structured_output(AnalysisResponse)
        
        template = """Vous êtes un analyste médical expert. Analysez le contexte suivant pour répondre à la question.
Si des outils externes sont mentionnés comme disponibles, suggérez leur utilisation dans l'analyse.

Contexte : {context}
Outils suggérés : {tool_results}
Question : {question}

Fournissez une analyse structurée complète."""
        
        prompt = PromptTemplate(template=template, input_variables=["context", "question", "tool_results"])
        chain = prompt | structured_llm
        result = chain.invoke({"context": context, "question": question, "tool_results": tool_results})
        
        return {"analysis": result.dict() if hasattr(result, 'dict') else result}

    except Exception as e:
        logger.error(f"Erreur Analyse : {e}")
        return {"analysis": {"detailed_analysis": f"Erreur technique : {str(e)}", "key_findings": [], "severity": "Erreur", "suggested_diagnoses": []}}
