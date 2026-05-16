import os
import asyncio
import aiofiles
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

from app.config import UPLOAD_DIR
from app.orchestrator import AgentOrchestrator
from app.rag.ingestor import ingest_document

app = FastAPI(
    title="AgentVault",
    description="Meridian Corp Intelligent Knowledge Assistant",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

orchestrator = AgentOrchestrator()


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


@app.get("/", response_class=HTMLResponse)
async def root():
    async with aiofiles.open("frontend/index.html", "r") as f:
        content = await f.read()
    return HTMLResponse(content=content)


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        response = await orchestrator.run(request.message, request.session_id)
        return {"response": response, "session_id": request.session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            message = data.get("message", "")
            session_id = data.get("session_id", "default")

            await websocket.send_json({"type": "start"})

            try:
                response = await orchestrator.run(message, session_id)
                for chunk in response.split(" "):
                    await websocket.send_json({"type": "token", "content": chunk + " "})
                    await asyncio.sleep(0.02)
                await websocket.send_json({"type": "end"})
            except Exception as e:
                await websocket.send_json({"type": "error", "content": str(e)})

    except WebSocketDisconnect:
        pass


@app.post("/api/documents")
async def upload_document(file: UploadFile = File(...)):
    allowed_extensions = {".txt", ".pdf", ".md", ".docx"}
    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"File type {file_ext} not supported")

    upload_path = Path(UPLOAD_DIR) / file.filename
    upload_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(upload_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    doc_count = ingest_document(str(upload_path))

    return JSONResponse({
        "status": "success",
        "filename": file.filename,
        "chunks_indexed": doc_count,
        "message": f"Document '{file.filename}' has been added to the knowledge base.",
    })


@app.get("/api/health")
async def health():
    return {"status": "healthy", "service": "AgentVault", "environment": os.environ.get("APP_ENV", "production")}


@app.get("/api/sessions/{session_id}/history")
async def get_history(session_id: str):
    history = orchestrator.get_history(session_id)
    return {"session_id": session_id, "history": history}


@app.delete("/api/sessions/{session_id}")
async def clear_session(session_id: str):
    orchestrator.clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}
