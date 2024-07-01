from pydantic import BaseModel
from typing import Any

from src.domain.entities.user import User

from src.models.user_model import UserModel

from sqlalchemy.future import select


class UserMapper(BaseModel):
    def to_model(user: User) -> UserModel:
        return UserModel(
            id=user.id,
            email=user.email,
            name=user.name,
            picture_url=user.picture_url,
            access_token=user.access_token,
            refresh_token=user.refresh_token,
        )

    def to_entity(user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            email=user_model.email,
            name=user_model.name,
            picture_url=user_model.picture_url,
            access_token=user_model.access_token,
            refresh_token=user_model.refresh_token,
        )


class UserRepo(BaseModel):
    session: Any

    async def save(self, user: User) -> User:
        user_model = UserMapper.to_model(user)
        self.session.add(user_model)
        await self.session.commit()
        return user

    async def fetch_user_by_id(self, user_id: str) -> User:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user_model = result.scalars().first()
        if user_model is None:
            return None
        return UserMapper.to_entity(user_model)
