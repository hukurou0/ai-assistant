from pydantic import BaseModel
from src.domain.entities.todo import Todo
from datetime import datetime


class SelectedTodo(BaseModel):
  id:str
  todo:Todo
  start:datetime
  end:datetime
        
  def __str__(self):
    return f"todo:{self.todo}, start:{self.start}, end:{self.end}"