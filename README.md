# 🩺 Medical Multi-Agent Assistant

Ce projet universitaire implémente un système multi-agents intelligent aidant les professionnels de la santé à analyser des documents médicaux privés (PDF, TXT, CSV) via une architecture **Multi-Agents** et un pipeline **RAG** (Retrieval-Augmented Generation) fonctionnant à **100% en local**.

## 🌟 Caractéristiques et Contraintes Respectées
- **100% Local & Sécurisé** : Utilisation exclusive du modèle `Llama 3` via Ollama. Aucune donnée n'est envoyée à une API externe (OpenAI, Anthropic, etc.).
- **Pipeline RAG Complet** : Ingestion, chunking, embeddings locaux (Ollama) et Vector Store avec **ChromaDB**. Utilisation intégrale de **LlamaIndex**.
- **Architecture Multi-Agents** : Développée avec **LangChain** et orchestrée via **LangGraph**. Le système utilise un état partagé pour gérer 4 agents experts.
- **Interface Utilisateur Moderne** : Application développée avec **Streamlit** pour un usage immédiat.

## 🧠 Architecture Multi-Agents (Orchestration LangGraph)

Le flux de traitement est strictement séquentiel et orchestré par LangGraph.
1. **Agent 1 : Medical Retrieval Agent** - Cherche le contexte pertinent dans ChromaDB en utilisant LlamaIndex.
2. **Agent 2 : Medical Analysis Agent** - Utilise LangChain pour analyser les symptômes, détecter les maladies et extraire l'expertise médicale.
3. **Agent 3 : Medical Report Agent** - Structure un rapport médical officiel (Résumé, Symptômes, Analyse, Recommandation).
4. **Agent 4 : Validation Agent** - Relecteur final qui vérifie l'absence d'hallucination et la conformité de la réponse.

---

## 🏗 Structure du Projet
```text
medical_multi_agent/
├── app.py                       # Point d'entrée FastAPI
├── requirements.txt             # Liste des dépendances
├── README.md                    # Documentation complète
├── .env.example                 # Modèle de variables d'environnement
├── data/                        # Dossier pour les documents bruts (TXT de test inclus)
├── agents/                      # Dossier des Agents LangChain
│   ├── retrieval_agent.py
│   ├── analysis_agent.py
│   ├── report_agent.py
│   ├── validation_agent.py
├── rag/                         # Pipeline LlamaIndex
│   ├── ingest.py
│   ├── index_builder.py
│   ├── retriever.py
├── orchestrator/                # Orchestration
│   ├── workflow.py              # Configuration du StateGraph LangGraph
├── ui/                          # Interface graphique
│   ├── streamlit_app.py
├── utils/                       # Utilitaires globaux
│   ├── config.py
│   ├── logger.py
├── vectorstore/                 # Base de données vectorielle
│   ├── chroma_store.py
```

---

## 🚀 Installation & Lancement Rapide

### 1. Pré-requis Obligatoires
- Python 3.9+
- **Ollama** installé sur votre machine : [Télécharger Ollama](https://ollama.com/)

### 2. Téléchargement du Modèle Local
Ouvrez un terminal et exécutez cette commande pour télécharger le LLM :
```bash
ollama pull llama3
```
*(Remarque : Ollama doit être en cours d'exécution en arrière-plan pendant l'utilisation de l'application)*

### 3. Installation des dépendances
Ouvrez un terminal dans le dossier du projet (`medical_multi_agent`) et exécutez :
```bash
pip install -r requirements.txt
```

### 4. Configuration
*(Facultatif mais recommandé)* Copiez le fichier d'exemple d'environnement :
```bash
cp .env.example .env
```

### 5. Ingestion Initiale des Documents
Un dossier patient fictif est déjà présent (`data/patient_record_fictional.txt`).
Générez l'index vectoriel ChromaDB avec la commande :
```bash
python -m rag.ingest
```

### 6. Lancement de l'Application
Lancez l'interface Streamlit :
```bash
streamlit run ui/streamlit_app.py
```
L'interface web s'ouvrira automatiquement. Vous pouvez y déposer de nouveaux fichiers PDF/TXT et poser vos questions médicales.

*(Optionnel)* Si vous souhaitez utiliser le système en tant qu'API REST, lancez FastAPI :
```bash
uvicorn app:app --reload
```

---

## 👨‍🏫 Note pour la Soutenance
Ce projet est modulaire et *production-ready*. 
- **Sécurité** : Les documents ne sortent jamais du poste de travail. 
- **Explicabilité** : L'interface Streamlit permet de déplier les logs ("Détails de l'orchestration") pour observer le raisonnement spécifique de **chaque agent**, ce qui est parfait pour démontrer la valeur ajoutée d'un système Multi-Agents lors de la soutenance.
