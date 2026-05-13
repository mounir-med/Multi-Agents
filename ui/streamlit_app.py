import streamlit as st
import os
import sys

# Permet d'importer les modules du projet
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from orchestrator.workflow import process_question
from utils.config import DATA_DIR
from rag.ingest import ingest_data

st.set_page_config(page_title="Medical Multi-Agent Assistant", layout="wide", page_icon="🩺")

st.title("🩺 Medical Multi-Agent Assistant")
st.markdown("Système d'analyse de documents médicaux par intelligence artificielle multi-agents (RAG local via Ollama & LangGraph).")

# Initialisation de la mémoire pour l'historique
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar pour la gestion des données RAG
with st.sidebar:
    st.header("📂 Gestion des Documents Médicaux")
    st.markdown("Ajoutez des dossiers (PDF, TXT, CSV) à analyser.")
    
    uploaded_files = st.file_uploader("Uploadez des fichiers", accept_multiple_files=True)
    
    if st.button("Ingérer et Indexer les documents"):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
        
        # Sauvegarde des fichiers localement
        saved_paths = []
        if uploaded_files:
            for f in uploaded_files:
                file_path = os.path.join(DATA_DIR, f.name)
                with open(file_path, "wb") as f_out:
                    f_out.write(f.read())
                saved_paths.append(file_path)
            st.success(f"{len(uploaded_files)} fichier(s) uploadé(s).")
            
        with st.spinner("Ingestion RAG et création de l'index ChromaDB en cours..."):
            ingest_data(input_files=saved_paths if saved_paths else None)
        st.success("Ingestion terminée ! Base vectorielle mise à jour.")

# Zone principale
st.header("💬 Poser une question sur les dossiers")

available_docs = []
if os.path.exists(DATA_DIR):
    available_docs = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]

selected_doc = ""
if available_docs:
    selected_doc = st.selectbox(
        "Limiter la recherche à un document (optionnel)",
        options=[""] + sorted(available_docs),
        format_func=lambda x: "Tous les documents" if x == "" else x,
    )

question = st.text_input("Exemple : Quels sont les symptômes importants et la recommandation présents dans le dossier patient ?")

if st.button("Lancer l'Analyse Multi-Agents"):
    if question.strip():
        with st.spinner("Orchestration en cours : Retrieval -> Analysis -> Report -> Validation..."):
            try:
                # Appel au workflow LangGraph
                result = process_question(question, document_filter=selected_doc)
                
                # Mise à jour historique
                st.session_state.history.append({
                    "q": question, 
                    "r": result["final_output"], 
                    "confidence": result["validation_status"]
                })
                
                st.subheader("📝 Réponse Finale Validée")
                st.write(result["final_output"])
                
                st.caption(f"Status: {result['validation_status']}")
                
                # Transparence / Explicabilité des agents
                with st.expander("🔍 Voir les détails techniques de l'orchestration (Logs Agents)"):
                    st.markdown("### 🤖 Agent 1 : Medical Retrieval")
                    st.info(result["retrieved_context"][:1000] + "\n[...]" if len(result["retrieved_context"]) > 1000 else result["retrieved_context"])
                    
                    st.markdown("### 🤖 Agent 2 : Medical Analysis")
                    st.success(result["analysis"])
                    
                    st.markdown("### 🤖 Agent 3 : Medical Report")
                    st.warning(result["report"])
                    
            except Exception as e:
                st.error(f"Une erreur est survenue lors de l'exécution : {e}")
    else:
        st.error("Veuillez saisir une question avant de lancer l'analyse.")

# Affichage de l'historique
if st.session_state.history:
    st.divider()
    st.header("🕒 Historique de session")
    for idx, chat in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Question : {chat['q']}"):
            st.write(chat['r'])
            st.caption(f"Confidence: {chat.get('confidence', 'N/A')}")
