# Interface Médicale Multi-Agents (Next.js)

Cette nouvelle interface remplace l'ancienne interface Streamlit par une application web moderne et professionnelle développée avec Next.js 15.

## Prérequis

1.  **Backend (Python)** : Assurez-vous que le serveur FastAPI est lancé.
2.  **Ollama** : Doit être en cours d'exécution localement.

## Lancement du Projet

### 1. Lancer le Backend
Depuis la racine du projet (`Multi-Agents`), exécutez :
```bash
python app.py
```
Le serveur sera accessible sur `http://localhost:8000`.

### 2. Lancer le Frontend
Ouvrez un nouveau terminal, allez dans le dossier `frontend` et lancez le serveur de développement :
```bash
cd frontend
npm run dev
```
L'interface sera accessible sur `http://localhost:3000`.

## Fonctionnalités
- **Design Professionnel** : Palette de couleurs médicale, interface épurée et moderne.
- **Suivi en temps réel** : Visualisation du workflow multi-agents (Recherche, Analyse, Rapport, Validation).
- **Entièrement Local** : Utilise votre instance Ollama et ChromaDB.
- **Responsive** : Adapté aux différents écrans.
