from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
  id:str
  title:str
  notes:str
  updated:str
  position:str
  status:str
  due:str
  difficulty:Optional[int] = None
  required_time:Optional[int] = None
  priority:Optional[int] = None
    
  def add_evaluation(self, evaluation_params):
    self.difficulty    = evaluation_params["difficulty"]
    self.required_time = evaluation_params["required_time"]
    self.priority      = evaluation_params["priority"]
    return self
    
        
  def __str__(self):
    if self.difficulty:
      return f"title:{self.title}, required_time:{self.required_time}, difficulty:{self.difficulty}"
    else:
      return f"title:{self.title}, difficulty:{None}"