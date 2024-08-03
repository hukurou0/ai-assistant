from pydantic import BaseModel


class SuggestTodoVO(BaseModel):
    id: str
    title: str
    required_time: int
    notes: str
    selected: bool
