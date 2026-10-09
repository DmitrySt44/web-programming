import json
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()

FILE_NAME = "students.json"


class StudentIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50)
    group: str = Field(default="", max_length=20)


def load_data():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(students, f, ensure_ascii=False, indent=2)


students = load_data()

next_id = 1
for s in students:
    if s["id"] >= next_id:
        next_id = s["id"] + 1


@app.get("/")
def home():
    return FileResponse("index.html")


@app.get("/students")
def get_students():
    return students


@app.post("/students")
def add_student(data: StudentIn):
    global next_id
    student = {"id": next_id, "name": data.name, "group": data.group}
    next_id += 1
    students.append(student)
    save_data()
    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            save_data()
            return {"message": "Удалено"}
    raise HTTPException(status_code=404, detail="Нет такого студента")

@app.put("/students/{student_id}")
def update_student(student_id: int, data: StudentIn):
    for student in students:
        if student["id"] == student_id:
            student["name"] = data.name
            student["group"] = data.group
            save_data()
            return student
    raise HTTPException(status_code=404, detail="Нет такого студента")