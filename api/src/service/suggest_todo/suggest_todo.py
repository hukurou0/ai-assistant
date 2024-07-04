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

    async def find_well_todos(
        self, user_id: str, free_time_id: str
    ) -> list[SuggestTodoVO]:
        user_repo = UserRepo(session=self.session)
        user = await user_repo.fetch_user_by_id(user_id)
        todos = await self.todo_provider.fetch_todos(user)

        free_time_repo = FreeTimeRepo(session=self.session)
        free_time = await free_time_repo.fetch_by_id(free_time_id)

        well_todos = DPAlgorithm(free_time=free_time, todos=todos).execute()

        return well_todos
