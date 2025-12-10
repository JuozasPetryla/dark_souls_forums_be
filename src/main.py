from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.api.v1.routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from collections import defaultdict
from typing import Dict, Set

app = FastAPI(title="FastAPI Starter")

app.mount("/static", StaticFiles(directory="/dark_souls_forums_be/src/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.exception_handler(HTTPException)
def custom_http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
        }
    )

# Store active viewers per topic
active_viewers: Dict[str, Set[WebSocket]] = defaultdict(set)

@app.websocket("/ws/topic/{topic_id}")
async def topic_viewer_websocket(websocket: WebSocket, topic_id: str):
    await websocket.accept()
    
    # Add this viewer to the topic
    active_viewers[topic_id].add(websocket)
    
    # Broadcast updated count to all viewers of this topic
    await broadcast_viewer_count(topic_id)
    
    try:
        # Keep connection alive and listen for disconnect
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Remove viewer when they disconnect
        active_viewers[topic_id].discard(websocket)
        await broadcast_viewer_count(topic_id)
        
        # Clean up empty topics
        if not active_viewers[topic_id]:
            del active_viewers[topic_id]

async def broadcast_viewer_count(topic_id: str):
    count = len(active_viewers[topic_id])
    message = f"{count}"
    
    # Send count to all connected viewers
    disconnected = set()
    for connection in active_viewers[topic_id]:
        try:
            await connection.send_text(message)
        except:
            disconnected.add(connection)
    
    # Clean up any dead connections
    active_viewers[topic_id] -= disconnected