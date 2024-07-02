from src.domain.entities.free_time import FreeTime
from src.domain.entities.todo import Todo
from src.domain.vos.suggest_todo_vo import SuggestTodoVO

from pydantic import BaseModel


class ConvertedTodo(BaseModel):
    id: str
    value: float
    time: int

    def __str__(self):
        return f"id: {self.id}, value: {self.value}, time: {self.time}"


class GreedyAlgorithm:
    def __init__(self, free_time: FreeTime, todos: list[Todo]):
        self.free_time = free_time
        self.todos = todos
        self.__converted_todos: list[ConvertedTodo] = []

    def __convert_todos(self):
        for todo in self.todos:
            if todo.required_time and todo.priority:
                value = todo.priority / todo.required_time
                self.__converted_todos.append(
                    ConvertedTodo(id=todo.id, value=value, time=todo.required_time)
                )
        self.__converted_todos.sort(key=lambda todo: todo.value, reverse=True)

    def __revert(self, converted_todo: ConvertedTodo) -> Todo:
        for todo in self.todos:
            if todo.id == converted_todo.id:
                return todo

    def execute(self):
        self.__convert_todos()

        well_todos: list[SuggestTodoVO] = []
        duration = self.free_time.get_duration()
        for i, converted_todo in enumerate(self.__converted_todos):
            todo = self.__revert(converted_todo)
            if duration >= todo.required_time:
                well_todos.append(SuggestTodoVO(free_time=self.free_time, todo=todo))
                duration -= todo.required_time

        return well_todos
