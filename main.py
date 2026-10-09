from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from controllers import StudentController
from realtime import ConnectionManager
from repositories import JsonStudentRepo
from services import NaiveStudentService

app = FastAPI()

# Здесь (и только здесь) решается, из каких деталей собрано приложение.
# Хотите другое хранилище или другой сервис — меняйте строки ниже.
repo = JsonStudentRepo("students.json")
service = NaiveStudentService(repo)
manager = ConnectionManager()
controller = StudentController(service, manager)

app.include_router(controller.router)


@app.get("/")
def home():
    return FileResponse("index.html")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # сами страницы ничего не присылают, мы просто ждём, пока соединение закроется
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
