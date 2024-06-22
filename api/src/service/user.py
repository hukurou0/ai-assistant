from pydantic import BaseModel
from typing import Any

from src.domain.entities.user import User

from src.service.shared.provider.oauth import OAuthProvider
from src.service.shared.provider.jwt import JWTProvider
from src.repository.user_repo import UserRepo

class UserService(BaseModel):
  session:Any
  
  async def signup(self, access_token, refresh_token)->str:
    userinfo = await OAuthProvider().fetch_userinfo(access_token)
    user = User(
      id          = userinfo["id"], 
      email       = userinfo["email"], 
      name        = userinfo["name"], 
      picture_url = userinfo["picture"],
      access_token  = access_token,
      refresh_token = refresh_token
      )
    repo = UserRepo(session=self.session)
    await repo.save(user)
    tokens = await JWTProvider().get_jwt_from_user_id(user.id)
    return tokens