import os
import json
import asyncio
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator.workflow import build_workflow, process_question
from rag.ingest import ingest_data
from utils.config import DATA_DIR

app = FastAPI(
    title="Medical Multi-Agent API", 
    description="API REST pour le système multi-agents d'analyse médicale (RAG 100% Local).",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    document_filter: str = ""

@app.post("/api/ask")
def ask_question(request: QueryRequest):
    result = process_question(request.question, document_filter=request.document_filter)
    return {
        "question": request.question, 
        "validation_status": result.get("validation_status", ""),
        "response": result.get("final_output", "Erreur lors de la génération.")
    }

@app.get("/api/ask-stream")
async def ask_stream(question: str, document_filter: str = ""):
    """
    Envoie les étapes de l'orchestration en temps réel via SSE.
    """
    async def event_generator():
        workflow = build_workflow()
        initial_state = {
            "question": question,
            "document_filter": document_filter or "",
            "retrieved_context": "",
            "retrieved_passages": [],
            "analysis": "",
            "report": "",
            "validation_status": "",
            "final_output": ""
        }
        
        try:
            final_state = initial_state
            for output in workflow.stream(initial_state):
                for node_name, state_delta in output.items():
                    final_state.update(state_delta)
                    
                    step_map = {
                        "retrieval_agent": "retrieval",
                        "analysis_agent": "analysis",
                        "report_agent": "report",
                        "validation_agent": "validation"
                    }
                    ui_node = step_map.get(node_name, node_name)
                    
                    # On envoie aussi les données partielles pour l'affichage progressif
                    payload = {
                        'node': ui_node, 
                        'status': 'complete',
                        'data': state_delta.get('analysis') or state_delta.get('report') or state_delta.get('retrieved_context')
                    }
                    yield f"data: {json.dumps(payload)}\n\n"
                await asyncio.sleep(0.1)

            # Envoi du résultat final collecté pendant le stream
            final_payload = {
                'node': 'final', 
                'output': final_state.get('final_output', final_state.get('report', '')), 
                'validation': final_state.get('validation_status', ''),
                'audit': final_state.get('audit_results', {})
            }
            yield f"data: {json.dumps(final_payload)}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    ingest_data(input_files=[file_path])
    return {"filename": file.filename, "status": "Indexed successfully"}

@app.get("/api/files")
def list_files():
    if not os.path.exists(DATA_DIR): return {"files": []}
    files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
    return {"files": files}

@app.delete("/api/delete/{filename}")
def delete_file(filename: str):
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"status": "success", "message": f"File {filename} deleted"}
    return {"status": "error", "message": "File not found"}, 404

@app.get("/api/health")
def health_check():
    return {"status": "Système Multi-Agents Médical Opérationnel"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
