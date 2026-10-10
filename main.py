from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from controllers import StudentController
from realtime import ConnectionManager
from repositories import JsonStudentRepo
from services import NaiveStudentService

app = FastAPI()
repo = JsonStudentRepo("students.json")
service = NaiveStudentService(repo)
manager = ConnectionManager()
controller = StudentController(service, manager)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(controller.router)


@app.get("/")
def home():
    return FileResponse("index.html")


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await manager.connect(websocket)
#     try:
#         while True:
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
