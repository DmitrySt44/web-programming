from fastapi import WebSocket


class ConnectionManager:
    """Помнит все открытые страницы (WebSocket-соединения) и умеет написать им всем сразу."""

    def __init__(self):
        self.connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self, message: str):
        for websocket in list(self.connections):
            try:
                await websocket.send_text(message)
            except Exception:
                # страница уже закрыта — просто забываем о ней
                self.disconnect(websocket)
