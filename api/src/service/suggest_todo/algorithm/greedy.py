from src.domain.entities.free_time import FreeTime
from src.domain.entities.todo import Todo
from src.domain.vos.suggest_todo_vo import SuggestTodoVO
from src.domain.vos.converted_todo_vo import ConvertedTodoVO

from src.service.suggest_todo.algorithm.util.handle_todo import (
    convert_todos,
    revert_todo,
)


class GreedyAlgorithm:
    def __init__(self, free_time: FreeTime, todos: list[Todo]):
        self.free_time = free_time
        self.todos = todos
        self.__converted_todos: list[ConvertedTodoVO] = []
        self.well_todos: list[SuggestTodoVO] = []

    def _culc_value(self, todo: Todo) -> float:
        return todo.priority / todo.required_time

    def execute(self) -> list[SuggestTodoVO]:
        self.__converted_todos = convert_todos(self.todos, self._culc_value)

        duration = self.free_time.get_duration()
        for converted_todo in self.__converted_todos:
            todo = revert_todo(converted_todo, self.todos)
            if duration >= todo.required_time:
                self.well_todos.append(
                    SuggestTodoVO(free_time=self.free_time, todo=todo)
                )
                duration -= todo.required_time

        return self.well_todos
