# 🩺 Système Expert Médical Multi-Agents

Une application clinique moderne de type **EPR (Electronic Patient Record)**, pilotée par un système multi-agents intelligent. Ce projet permet d'analyser des documents médicaux (PDF, TXT, images) de manière sécurisée grâce à une architecture **RAG** (Retrieval-Augmented Generation) fonctionnant à **100% en local**.

---

## ✨ Fonctionnalités Principales
- **Confidentialité Totale (100% Local)** : L'IA tourne sur votre propre machine grâce à **Ollama** (modèles `llama3.2`, `llava`, `nomic-embed-text`). Aucune fuite de données patient.
- **Architecture Multi-Agents** : Orchestration via **LangGraph** de 4 agents spécialisés :
  1. **Agent Retrieval** : Recherche sémantique dans la base documentaire locale (ChromaDB + LlamaIndex).
  2. **Agent Analyse** : Examen clinique textuel et visuel (Vision IA) de pointe.
  3. **Agent Rapport** : Génération structurée d'un bilan de santé complet.
  4. **Agent Validation** : Audit automatique anti-hallucination.
- **Interface Next.js Premium** : Design de qualité clinique (Glassmorphism, animations fluides Framer Motion, layout EPR).
- **Synchronisation Temps Réel** : Suivi visuel du raisonnement des agents via **SSE (Server-Sent Events)**.
- **Audit & Validation** : Tableau de bord de surveillance pour les rapports générés et flux de validation humaine ("Approuvé par le médecin").
- **Génération de PDF Officiels** : Export professionnel des rapports de diagnostic.

---

## 🏗️ Architecture du Projet

```text
medical_multi_agent/
├── app.py                       # Backend API (FastAPI) principal
├── requirements.txt             # Dépendances Python
├── .env                         # Configuration des modèles
├── data/                        # Dossier des dossiers médicaux bruts
├── frontend/                    # Interface graphique Moderne (Next.js 14)
│   ├── src/app/                 # Pages, layout, CSS global
│   ├── src/components/          # Composants React (Documents, Surveillance...)
│   └── package.json             # Dépendances Node.js
├── agents/                      # Logique des Agents LangChain
├── rag/                         # Moteur LlamaIndex et Ingestion
├── orchestrator/                # Orchestration du StateGraph
├── utils/                       # Utilitaires (config, logger)
└── vectorstore/                 # Base de données vectorielle ChromaDB
```

---

## 🚀 Guide d'Installation

### 1. Pré-requis Système
- **Python 3.9+**
- **Node.js 18+** (pour le frontend Next.js)
- **Ollama** installé sur votre machine : [Télécharger Ollama](https://ollama.com/)

### 2. Téléchargement des Modèles Locaux
Assurez-vous qu'Ollama est en cours d'exécution, puis lancez :
```bash
ollama pull llama3.2
ollama pull llava
ollama pull nomic-embed-text
```

### 3. Installation du Backend (Python)
Dans le dossier racine du projet :
```bash
# Optionnel: créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sous Windows: venv\Scripts\activate

# Installation des dépendances
pip install -r requirements.txt

# (Optionnel) Copier la config
cp .env.example .env
```

### 4. Installation du Frontend (Next.js)
```bash
cd frontend
npm install
# ou
yarn install
```

---

## 🎮 Lancement de l'Application

Vous devez lancer le backend et le frontend simultanément (dans deux terminaux différents).

### Terminal 1 : Le Backend (FastAPI)
Depuis la racine du projet :
```bash
python app.py
# L'API tourne sur http://localhost:8000
```

### Terminal 2 : Le Frontend (Next.js)
Depuis le dossier `frontend/` :
```bash
npm run dev
# L'interface tourne sur http://localhost:3000
```

Ouvrez **[http://localhost:3000](http://localhost:3000)** dans votre navigateur pour accéder au système.

---

## 👨‍⚕️ Flux d'Utilisation Typique
1. Naviguez vers l'onglet **Documents** pour uploader des PDF de patients ou des images (radios, lésions cutanées).
2. Retournez sur le **Dashboard Clinique**.
3. Sélectionnez le document en cliquant sur l'icône Dossier de la barre de chat.
4. Demandez à l'assistant d'analyser le document ("Fais une analyse complète", "Que vois-tu sur cette image ?").
5. Suivez le raisonnement en temps réel.
6. Une fois le rapport généré, cliquez sur **Valider** pour l'approuver ou **PDF** pour l'exporter en document officiel.
7. Allez dans l'onglet **Surveillance** pour un audit global de la base.

---

*Projet conçu avec ❤️ pour révolutionner l'assistance médicale par l'IA locale.*
