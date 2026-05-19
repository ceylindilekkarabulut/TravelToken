from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

connected_clients: dict[str, list[WebSocket]] = {}


@router.websocket("/notifications/{wallet}")
async def ws_notifications(websocket: WebSocket, wallet: str):
    await websocket.accept()
    connected_clients.setdefault(wallet, []).append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients[wallet].remove(websocket)


async def push_notification(wallet: str, message: dict):
    for ws in connected_clients.get(wallet, []):
        try:
            await ws.send_json(message)
        except Exception:
            pass
