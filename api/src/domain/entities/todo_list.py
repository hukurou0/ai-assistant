from pydantic import BaseModel
from src.domain.vos.todo import TodoVO

class TodoList(BaseModel, frozen=True):
  id:str
  title:str
  updated:str
  todos:list[TodoVO]
  