from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload

from pydantic import BaseModel
from typing import Any
from src.models.tag_model import TagModel
from src.domain.entities.tag import Tag
from src.domain.entities.user import User


class TagMapper:
    @staticmethod
    def to_model(tag_entity: Tag) -> TagModel:
        return TagModel(tag_entity=tag_entity)

    @staticmethod
    def to_entity(tag_model: TagModel, user: User) -> Tag:
        return Tag(id=tag_model.id, name=tag_model.name, user=user)


class TagRepo(BaseModel):
    session: Any

    async def create(self, tag_entity: Tag):
        todo_model = TagMapper.to_model(tag_entity)
        self.session.add(todo_model)
        await self.session.commit()

    async def find(self, tag_name: str, user_id: str) -> str | None:
        tag = await self.session.execute(
            select(TagModel).filter(
                TagModel.name == tag_name, TagModel.user_id == user_id
            )
        )
        tag_model = tag.scalars().first()
        tag = TagMapper.to_entity(tag_model) if tag_model else None
        return tag

    async def update(self, tag_entity: Tag):
        return

    async def delete(self):
        pass
