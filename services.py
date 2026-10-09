from abc import ABC, abstractmethod

from repositories import IStudentRepo


class IStudentService(ABC):
    """Интерфейс сервиса: что приложение умеет делать со студентами."""

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


class NaiveStudentService(IStudentService):
    """Самая простая реализация: ничего своего не добавляет,
    просто передаёт вызовы репозиторию.

    Репозиторий приходит в конструктор снаружи (r: IStudentRepo),
    сервис не знает, JSON это, Postgres или что-то ещё.
    """

    def __init__(self, repo: IStudentRepo):
        self.repo = repo

    def get_students(self):
        return self.repo.get_students()

    def get_student_by_id(self, student_id):
        return self.repo.get_student_by_id(student_id)

    def add_student(self, name, group):
        return self.repo.add_student(name, group)

    def update_student(self, student_id, name, group):
        return self.repo.update_student(student_id, name, group)

    def delete_student(self, student_id):
        return self.repo.delete_student(student_id)
