from pydantic import BaseModel

import jwt
import os

#TODO# #MUST#  トークンに有効期限を設定する
# リフレッシュトークンの有効期限を長めに設定する
# リフレッシュトークンが使用されるたびに新しいリフレッシュトークンを発行し、古いトークンを無効にする
class JWTProvider(BaseModel):
  async def get_jwt_from_user_id(self, user_id:str) -> str:
    payload = {
        'user_id': user_id,
    }
    token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm='HS256')
    return token
  
  async def get_user_id_from_token(self, token) -> str:
    try:
      payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=['HS256'])
      return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None  # トークンの有効期限が切れている場合
    except jwt.InvalidTokenError:
        return None  # トークンが無効な場合