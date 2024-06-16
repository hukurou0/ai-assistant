from pydantic import BaseModel
from typing import Any

from src.domain.entities.user import User

from src.models.user_model import UserModel

class UserRepo(BaseModel):
  session:Any
  
  async def save(self, user:User) -> User:
    new_user = UserModel(
      id            = user.id,
      email         = user.email,
      name          = user.name,
      picture_url   = user.picture_url,
      access_token  = user.access_token,
      refresh_token = user.refresh_token,
    )
    self.session.add(new_user)
    await self.session.commit()
    return user
  
  async def fetch_by_id(self, user_id:str) -> User:
    # tokenは取得しない
    pass