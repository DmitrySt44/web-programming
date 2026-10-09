import json
import os
from abc import ABC, abstractmethod


class IStudentRepo(ABC):
    """Интерфейс: список методов, которые умеет любое хранилище студентов.

    Сам по себе он ничего не делает, он только говорит
    «любой репозиторий обязан уметь вот это».
    """

    @abstractmethod
    def get_students(self):
        ...

    @abstractmethod
    def get_student_by_id(self, student_id):
        ...

    @abstractmethod
    def add_student(self, name, group):
        ...

    @abstractmethod
    def update_student(self, student_id, name, group):
        ...

    @abstractmethod
    def delete_student(self, student_id):
        ...


class JsonStudentRepo(IStudentRepo):
    """Хранит студентов в файле students.json (раньше это было в main.py)."""

    def __init__(self, file_name="students.json"):
        self.file_name = file_name
        self.students = self.load_data()

        self.next_id = 1
        for s in self.students:
            if s["id"] >= self.next_id:
                self.next_id = s["id"] + 1

    def load_data(self):
        if not os.path.exists(self.file_name):
            return []
        with open(self.file_name, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_data(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(self.students, f, ensure_ascii=False, indent=2)

    def get_students(self):
        return self.students

    def get_student_by_id(self, student_id):
        for student in self.students:
            if student["id"] == student_id:
                return student
        return None

    def add_student(self, name, group):
        student = {"id": self.next_id, "name": name, "group": group}
        self.next_id += 1
        self.students.append(student)
        self.save_data()
        return student

    def update_student(self, student_id, name, group):
        student = self.get_student_by_id(student_id)
        if student is None:
            return None
        student["name"] = name
        student["group"] = group
        self.save_data()
        return student

    def delete_student(self, student_id):
        student = self.get_student_by_id(student_id)
        if student is None:
            return False
        self.students.remove(student)
        self.save_data()
        return True


class InMemoryStudentRepo(IStudentRepo):
    """Хранит студентов только в памяти, без файла (после перезапуска всё пропадёт).

    Нужен, чтобы убедиться: хранилище можно заменить, не трогая сервис и контроллер.
    По тому же принципу потом можно написать PostgresStudentRepo или MySqlStudentRepo.
    """

    def __init__(self):
        self.students = []
        self.next_id = 1

    def get_students(self):
        return self.students

    def get_student_by_id(self, student_id):
        for student in self.students:
            if student["id"] == student_id:
                return student
        return None

    def add_student(self, name, group):
        student = {"id": self.next_id, "name": name, "group": group}
        self.next_id += 1
        self.students.append(student)
        return student

    def update_student(self, student_id, name, group):
        student = self.get_student_by_id(student_id)
        if student is None:
            return None
        student["name"] = name
        student["group"] = group
        return student

    def delete_student(self, student_id):
        student = self.get_student_by_id(student_id)
        if student is None:
            return False
        self.students.remove(student)
        return True
