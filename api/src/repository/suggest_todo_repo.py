from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload

from src.models.suggest_todo_model import SuggestTodoModel

from pydantic import BaseModel
from typing import Any
from src.domain.entities.suggest_todo import SuggestTodos, SuggestTodo
from src.domain.entities.tag import Tag
from src.domain.entities.user import User
from src.models.tag_model import TagModel

from src.repository.todo_repo import TodoMapper
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

    def to_entity(
        suggest_model: list[SuggestTodoModel], user, tag_id_entity_map
    ) -> SuggestTodos:
        return SuggestTodos(
            free_time=FreeTimeMapper.to_entity(suggest_model[0].free_time),
            suggest_todos=[
                SuggestTodo(
                    id=suggest_todo.id,
                    todo=TodoMapper.to_entity(
                        suggest_todo.todo, user, tag_id_entity_map
                    ),
                    selected=suggest_todo.selected,
                )
                for suggest_todo in suggest_model
            ],
        )


class SuggestTodoRepo(BaseModel):
    session: Any

    async def fetch_by_free_time(
        self, free_time_id: str, user: User
    ) -> SuggestTodos | None:
        stmt = (
            select(SuggestTodoModel)
            .where(SuggestTodoModel.free_time_id == free_time_id)
            .options(
                joinedload(SuggestTodoModel.free_time),
                joinedload(SuggestTodoModel.todo),
            )
        )
        result = await self.session.execute(stmt)
        suggest_todo_models: list[SuggestTodoModel] = result.scalars().all()
        tag_id_entity_map = await self._fetch_tag_id_entity_map(
            {
                tag_id
                for suggest_todo in suggest_todo_models
                for tag_id in suggest_todo.todo.tag_ids
            },
            user,
        )
        if suggest_todo_models:
            return SuggestTodoMapper.to_entity(
                suggest_todo_models, user, tag_id_entity_map
            )
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

    async def _fetch_tag_id_entity_map(
        self, tag_ids: set[str], user: User
    ) -> dict[str, str]:
        stmt = select(TagModel).where(TagModel.id.in_(tag_ids))
        result = await self.session.execute(stmt)
        todo_models: list[TagModel] = result.scalars().all()
        tag_id_entity_map = {
            tag_model.id: Tag(
                id=tag_model.id,
                name=tag_model.name,
                user=user,
            )
            for tag_model in todo_models
        }
        return tag_id_entity_map
