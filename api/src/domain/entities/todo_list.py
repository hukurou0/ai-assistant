from pydantic import BaseModel
from src.domain.entities.todo import Todo
from typing import Optional
import datetime

class TodoList(BaseModel):
  id:str
  title:str
  updated:datetime.datetime
  last_evaluation:Optional[datetime.datetime] = None
  todos:Optional[list[Todo]] = None
  
  def __str__(self):
    return f"TodoList(id={self.id}, title={self.title}, updated={self.updated}, last_evaluation={self.last_evaluation})"
  