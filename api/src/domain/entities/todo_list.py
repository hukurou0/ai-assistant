from pydantic import BaseModel
from src.domain.entities.todo import Todo

class TodoList(BaseModel, frozen=True):
  id:str
  title:str
  updated:str
  todos:list[Todo]
  