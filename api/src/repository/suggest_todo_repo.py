from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload

from src.models.suggest_todo_model import SuggestTodoModel

from pydantic import BaseModel
from typing import Any
from src.domain.entities.suggest_todo import SuggestTodos, SuggestTodo

from src.repository.todo_list_repo import TodoMapper
from src.repository.free_time_repo import FreeTimeMapper


class SuggestTodoMapper:
    @staticmethod
    def to_model(suggest_todos: SuggestTodos) -> list[SuggestTodoModel]:
        return [
            SuggestTodoModel(
                id=suggest_todo.id,
                todo_id=suggest_todo.todo.id,
                free_time_id=suggest_todos.free_time.id,
                selected=suggest_todo.selected,
            )
            for suggest_todo in suggest_todos.suggest_todos
        ]

    def to_entity(suggest_model: list[SuggestTodoModel]) -> SuggestTodos:
        return SuggestTodos(
            free_time=FreeTimeMapper.to_entity(suggest_model[0].free_time),
            suggest_todos=[
                SuggestTodo(
                    id=suggest_todo.id,
                    todo=TodoMapper.to_entity(suggest_todo.todo),
                    selected=suggest_todo.selected,
                )
                for suggest_todo in suggest_model
            ],
        )


class SuggestTodoRepo(BaseModel):
    session: Any

    async def fetch_by_free_time(self, free_time_id: str) -> SuggestTodos | None:
        stmt = (
            select(SuggestTodoModel)
            .where(SuggestTodoModel.free_time_id == free_time_id)
            .options(
                joinedload(SuggestTodoModel.free_time),
                joinedload(SuggestTodoModel.todo),
            )
        )
        result = await self.session.execute(stmt)
        suggest_todo_models = result.scalars().all()
        if suggest_todo_models:
            return SuggestTodoMapper.to_entity(suggest_todo_models)
        return None

    async def save(self, suggest_todos: SuggestTodos) -> None:
        suggest_todo_models = SuggestTodoMapper.to_model(suggest_todos)
        for suggest_todo_model in suggest_todo_models:
            self.session.add(suggest_todo_model)
        await self.session.commit()
        return None

    async def set_selected(self, suggest_todo_id: str, selected: bool):
        stmt = (
            update(SuggestTodoModel)
            .where(SuggestTodoModel.id == suggest_todo_id)
            .values(selected=selected)
        )
        await self.session.execute(stmt)
        await self.session.commit()
        return None
