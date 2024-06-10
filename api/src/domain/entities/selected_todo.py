from pydantic import BaseModel
from src.domain.entities.todo import Todo
from src.domain.entities.free_time import FreeTime


class SelectedTodo(BaseModel):
  id:str
  todo:Todo
  free_time:FreeTime
        
  def __str__(self):
    return f"todo:{self.todo}, free_time:{self.free_time}"