from fastapi import APIRouter, HTTPException

from models import StudentIn
from services import IStudentService


class StudentController:
    """Принимает HTTP-запросы по адресу /students и отдаёт работу сервису.

    Сервис приходит в конструктор снаружи (s: IStudentService),
    контроллер не знает, какой именно сервис и какое хранилище за ним стоят.
    """

    def __init__(self, service: IStudentService):
        self.service = service

        # APIRouter — это «набор адресов», который потом подключается к app
        self.router = APIRouter(prefix="/students")
        self.router.add_api_route("", self.get_students, methods=["GET"])
        self.router.add_api_route("", self.add_student, methods=["POST"])
        self.router.add_api_route("/{student_id}", self.update_student, methods=["PUT"])
        self.router.add_api_route("/{student_id}", self.delete_student, methods=["DELETE"])

    def get_students(self):
        return self.service.get_students()

    def add_student(self, data: StudentIn):
        return self.service.add_student(data.name, data.group)

    def update_student(self, student_id: int, data: StudentIn):
        student = self.service.update_student(student_id, data.name, data.group)
        if student is None:
            raise HTTPException(status_code=404, detail="Нет такого студента")
        return student

    def delete_student(self, student_id: int):
        if not self.service.delete_student(student_id):
            raise HTTPException(status_code=404, detail="Нет такого студента")
        return {"message": "Удалено"}
