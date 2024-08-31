from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload

from pydantic import BaseModel
from typing import Any
from src.models.todo_model import TodoModel
from src.domain.entities.todo import Todo
from src.domain.entities.user import User
from src.domain.entities.tag import Tag
from src.models.tag_model import TagModel


class TodoMapper:
    @staticmethod
    def to_model(todo_entity: Todo) -> TodoModel:
        return TodoModel(todo_entity=todo_entity)

    @staticmethod
    def to_entity(
        todo_model: TodoModel, user: User, tag_id_entity_map: dict[str, str]
    ) -> Todo:
        return Todo(
            id=todo_model.id,
            user=user,
            title=todo_model.title,
            notes=todo_model.notes,
            status=todo_model.status,
            due=todo_model.due,
            tags=[tag_id_entity_map[tag_id] for tag_id in todo_model.tag_ids],
            required_time=todo_model.required_time,
            priority_level=todo_model.priority_level,
            importance_level=todo_model.importance_level,
        )


class TodoRepo(BaseModel):
    session: Any

    async def create(self, todo_entity: Todo):
        todo_model = TodoMapper.to_model(todo_entity)
        self.session.add(todo_model)
        await self.session.commit()

    async def batch_create(self, todo_entities: list[Todo]):
        todo_models = [
            TodoMapper.to_model(todo_entity) for todo_entity in todo_entities
        ]
        self.session.add_all(todo_models)
        await self.session.commit()

    async def fetch_todo_by_id(self, todo_id: str) -> Todo | None:
        return

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

    async def fetch_todos_by_user(self, user: User) -> list[Todo]:
        stmt = select(TodoModel).where(TodoModel.user_id == user.id)
        result = await self.session.execute(stmt)
        todo_models: list[TodoModel] = result.scalars().all()
        tag_ids = set(
            tag_id for todo_model in todo_models for tag_id in todo_model.tag_ids
        )
        tag_id_entity_map = await self._fetch_tag_id_entity_map(tag_ids, user)
        todos = [
            TodoMapper.to_entity(todo_model, user, tag_id_entity_map)
            for todo_model in todo_models
        ]
        return todos

    async def update(self, todo_entity: Todo):
        return

    async def batch_updated(self, todo_entities: list[Todo]):
        for todo_entity in todo_entities:
            stmt = (
                update(TodoModel)
                .where(TodoModel.id == todo_entity.id)
                .values(
                    title=todo_entity.title,
                    notes=todo_entity.notes,
                    status=todo_entity.status,
                    due=todo_entity.due,
                    tag_ids=[tag.id for tag in todo_entity.tags],
                    required_time=todo_entity.required_time,
                    priority_level=todo_entity.priority_level,
                    importance_level=todo_entity.importance_level,
                )
            )
            await self.session.execute(stmt)
        await self.session.commit()

    async def delete(self):
        pass
