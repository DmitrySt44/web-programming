from fastapi import FastAPI
from fastapi.responses import FileResponse

from controllers import StudentController
from repositories import JsonStudentRepo
from services import NaiveStudentService

app = FastAPI()

# Здесь (и только здесь) решается, из каких деталей собрано приложение.
# Хотите другое хранилище или другой сервис — меняйте строки ниже.
repo = JsonStudentRepo("students.json")
service = NaiveStudentService(repo)
controller = StudentController(service)

app.include_router(controller.router)


@app.get("/")
def home():
    return FileResponse("index.html")
