from pydantic import BaseModel
from src.domain.entities.todo import Todo
from src.domain.entities.free_time import FreeTime


class SuggestTodoVO(BaseModel):
    free_time: FreeTime
    todo: Todo
