from src.service.shared.provider.local_todo import LocalTodoProvider

from typing import Union
from pydantic import BaseModel
from typing import Any
from src.domain.vos.suggest_todo_vo import SuggestTodoVO

from src.repository.free_time_repo import FreeTimeRepo
from src.repository.user_repo import UserRepo

from src.service.suggest_todo.algorithm.dynamic_programming import DPAlgorithm


class SuggestTodoService(BaseModel):
    session: Any
    todo_provider: Union[LocalTodoProvider]

    async def find_well_todos(self) -> list[SuggestTodoVO]:
        from src.repository.mock.todo.todos_to_object import load_todos_from_json
        from src.repository.mock.free_time.free_time_to_object import (
            load_free_time_from_json,
        )

        todos = load_todos_from_json("src/repository/mock/todo/todos.json")
        free_time = load_free_time_from_json(
            "src/repository/mock/free_time/free_time.json"
        )

        well_todos = DPAlgorithm(free_time=free_time, todos=todos).execute()

        return well_todos
