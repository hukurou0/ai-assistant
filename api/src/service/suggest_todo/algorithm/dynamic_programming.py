from src.domain.entities.free_time import FreeTime
from src.domain.entities.todo import Todo
from src.domain.vos.suggest_todo_vo import SuggestTodoVO
from src.domain.vos.converted_todo_vo import ConvertedTodoVO

import math

from src.service.suggest_todo.algorithm.util.handle_todo import (
    convert_todos,
    revert_todo,
)


class DPAlgorithm:
    def __init__(self, free_time: FreeTime, todos: list[Todo]):
        self.free_time = free_time
        self.todos = todos
        self.__converted_todos: list[ConvertedTodoVO] = []
        self.well_todos: list[SuggestTodoVO] = []

    def _culc_value(self, todo: Todo) -> float:
        importance_weight = 1.5
        priority_weight = 1.0
        importance_level = todo.importance_level * importance_weight
        priority_level = todo.priority_level * priority_weight
        required_time = math.log(todo.required_time + 1)
        return (importance_level - priority_level) / required_time

    def __knapsack(
        self, todos: list[ConvertedTodoVO], max_time: int
    ) -> list[ConvertedTodoVO]:
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

    def execute(self) -> list[Todo]:
        self.__converted_todos = convert_todos(self.todos, self._culc_value)

        duration = self.free_time.get_duration()
        converted_suggest_todos = self.__knapsack(self.__converted_todos, duration)

        suggest_todos = [
            revert_todo(converted_suggest_todo, self.todos)
            for converted_suggest_todo in converted_suggest_todos
        ]

        return suggest_todos
