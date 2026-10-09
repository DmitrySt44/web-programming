from fastapi import APIRouter, HTTPException

from models import StudentIn
from realtime import ConnectionManager
from services import IStudentService


class StudentController:

    def __init__(self, service: IStudentService, manager: ConnectionManager):
        self.service = service
        self.manager = manager
        self.router = APIRouter(prefix="/students")
        self.router.add_api_route("", self.get_students, methods=["GET"])
        self.router.add_api_route("", self.add_student, methods=["POST"])
        self.router.add_api_route("/{student_id}", self.update_student, methods=["PUT"])
        self.router.add_api_route("/{student_id}", self.delete_student, methods=["DELETE"])

    def get_students(self):
        return self.service.get_students()

    async def add_student(self, data: StudentIn):
        student = self.service.add_student(data.name, data.group)
        await self.manager.broadcast("changed")
        return student

    async def update_student(self, student_id: int, data: StudentIn):
        student = self.service.update_student(student_id, data.name, data.group)
        if student is None:
            raise HTTPException(status_code=404, detail="Нет такого студента")
        await self.manager.broadcast("changed")
        return student

    async def delete_student(self, student_id: int):
        if not self.service.delete_student(student_id):
            raise HTTPException(status_code=404, detail="Нет такого студента")
        await self.manager.broadcast("changed")
        return {"message": "Удалено"}
