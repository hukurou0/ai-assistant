from pydantic import BaseModel
from src.domain.entities.todo import Todo
from src.domain.vos.free_time import FreeTimeVO

class SuggestTodoVO(BaseModel):
    free_time: FreeTimeVO
    todo: Todo