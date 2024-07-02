from src.domain.entities.free_time import FreeTime
from src.domain.entities.todo import Todo
from src.domain.vos.suggest_todo_vo import SuggestTodoVO

from pydantic import BaseModel


class ConvertedTodo(BaseModel):
    id: str
    value: int
    time: int


class DPAlgorithm:
    def __init__(self, free_time: FreeTime, todos: list[Todo]):
        self.free_time = free_time
        self.todos = todos
        self.__converted_todos: list[ConvertedTodo] = []

    def __convert_todos(self):
        for todo in self.todos:
            if todo.required_time and todo.priority:
                self.__converted_todos.append(
                    ConvertedTodo(
                        id=todo.id, value=todo.priority, time=todo.required_time
                    )
                )

    def __knapsack(
        self, todos: list[ConvertedTodo], max_time: int
    ) -> list[ConvertedTodo]:
        n = len(todos)
        dp = [[0] * (max_time + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for w in range(max_time + 1):
                if todos[i - 1].time <= w:
                    dp[i][w] = max(
                        dp[i - 1][w],
                        dp[i - 1][w - todos[i - 1].time] + todos[i - 1].value,
                    )
                else:
                    dp[i][w] = dp[i - 1][w]

        w = max_time
        selected_todos = []
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                selected_todos.append(todos[i - 1])
                w -= todos[i - 1].time

        selected_todos.reverse()
        return selected_todos

    def __revert(self, converted_todo: ConvertedTodo) -> Todo:
        for todo in self.todos:
            if todo.id == converted_todo.id:
                return todo

    def execute(self):
        self.__convert_todos()

        well_todos: list[SuggestTodoVO] = []
        duration = self.free_time.get_duration()
        suggest_todos = self.__knapsack(self.__converted_todos, duration)
        for todo in suggest_todos:
            well_todo = SuggestTodoVO(
                free_time=self.free_time, todo=self.__revert(todo)
            )
            well_todos.append(well_todo)
        return well_todos
