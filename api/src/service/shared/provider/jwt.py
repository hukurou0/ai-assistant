from fastapi import HTTPException


from pydantic import BaseModel
from typing import Dict

import jwt
import os
import datetime
import pytz
from src.util.handle_time import get_now_datetime

ACCESS_TOKEN_EXPIRES_MINUTES = 15
REFRESH_TOKEN_EXPIRES_DAYS = 7


# TODO# #MUST#  トークンに有効期限を設定する
# リフレッシュトークンの有効期限を長めに設定する
# リフレッシュトークンが使用されるたびに新しいリフレッシュトークンを発行し、古いトークンを無効にする
class JWTProvider(BaseModel):
    async def get_jwt_from_user_id(self, user_id: str) -> str:
        payload = {
            "user_id": user_id,
        }
        now = get_now_datetime()
        expiration = now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
        access_token = jwt.encode(
            {"exp": expiration, **payload},
            os.getenv("JWT_SECRET_KEY"),
            algorithm="HS256",
        )
        expiration = now + datetime.timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS)
        refresh_token = jwt.encode(
            {"exp": expiration, **payload},
            os.getenv("JWT_SECRET_KEY"),
            algorithm="HS256",
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def get_user_id_from_token(self, token) -> str:
        try:
            payload = jwt.decode(
                token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"]
            )
            return payload["user_id"]
        except jwt.ExpiredSignatureError:
            return None  # トークンの有効期限が切れている場合
        except jwt.InvalidTokenError:
            return None  # トークンが無効な場合

    async def decode_jwt(token: str) -> Dict:
        try:
            payload = jwt.decode(
                token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
