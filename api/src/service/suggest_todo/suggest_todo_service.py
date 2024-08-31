from pydantic import BaseModel
from typing import Any
from src.domain.vos.suggest_todo_vo import SuggestTodoVO
from src.domain.entities.suggest_todo import SuggestTodo, SuggestTodos

from src.repository.free_time_repo import FreeTimeRepo
from src.repository.user_repo import UserRepo
from src.repository.todo_repo import TodoRepo
from src.repository.suggest_todo_repo import SuggestTodoRepo

from src.service.suggest_todo.algorithm.dynamic_programming import DPAlgorithm

from src.util.make_uuid import make_uuid


class SuggestTodoService(BaseModel):
    session: Any

    async def get_suggest_todos(
        self, user_id: str, free_time_id: str
    ) -> tuple[str, list[SuggestTodoVO]]:
        user_repo = UserRepo(session=self.session)
        user = await user_repo.fetch_user_by_id(user_id)
        suggest_todo_repo = SuggestTodoRepo(session=self.session)
        suggest_todos = await suggest_todo_repo.fetch_by_free_time(free_time_id, user)
        if suggest_todos:
            return free_time_id, suggest_todos.to_vos()
        else:
            suggest_todos = await self.find_well_todos(user_id, free_time_id)
            await suggest_todo_repo.save(suggest_todos)
            return free_time_id, suggest_todos.to_vos()

    async def find_well_todos(self, user_id: str, free_time_id: str) -> SuggestTodos:
        user_repo = UserRepo(session=self.session)
        todo_repo = TodoRepo(session=self.session)
        user = await user_repo.fetch_user_by_id(user_id)
        todos = await todo_repo.fetch_todos_by_user(user)

        free_time_repo = FreeTimeRepo(session=self.session)
        free_time = await free_time_repo.fetch_by_id(free_time_id)

        well_todos = DPAlgorithm(free_time=free_time, todos=todos).execute()

        suggest_todos = SuggestTodos(
            free_time=free_time,
            suggest_todos=[
                SuggestTodo(id=make_uuid(), todo=todo, selected=False)
                for todo in well_todos
            ],
        )

        return suggest_todos

    async def set_selected(self, suggest_todo_id: str, selected: bool):
        suggest_todo_repo = SuggestTodoRepo(session=self.session)
        await suggest_todo_repo.set_selected(suggest_todo_id, selected)
        return "success"
