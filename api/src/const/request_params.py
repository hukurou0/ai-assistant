from pydantic import BaseModel


class SuggestSelectParams(BaseModel):
    suggest_todo_id: str
    selected: bool


class SigninParams(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenParams(BaseModel):
    refresh_token: str
