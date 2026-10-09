from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

from repositories import JsonStudentRepo
from services import NaiveStudentService

app = FastAPI()

repo = JsonStudentRepo("students.json")
service = NaiveStudentService(repo)


class StudentIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    group: str = Field(default="", max_length=20)


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/students")
def get_students():
    return service.get_students()


@app.post("/students")
def add_student(data: StudentIn):
    return service.add_student(data.name, data.group)


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    if not service.delete_student(student_id):
        raise HTTPException(status_code=404, detail="Нет такого студента")
    return {"message": "Удалено"}


@app.put("/students/{student_id}")
def update_student(student_id: int, data: StudentIn):
    student = service.update_student(student_id, data.name, data.group)
    if student is None:
        raise HTTPException(status_code=404, detail="Нет такого студента")
    return student
