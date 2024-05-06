from pydantic import BaseModel
from src.domain.entities.todo import Todo
from typing import Optional

class TodoList(BaseModel):
  id:str
  title:str
  updated:str
  todos:Optional[list[Todo]] = None
  