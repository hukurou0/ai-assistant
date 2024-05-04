from src.service.llm.gpt.evaluation import fetch_evaluation_todo
from src.domain.vos.todo import TodoVO
from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
  id:str
  title:str
  notes:str
  updated:str
  difficulty:Optional[int] = None
  required_time:Optional[int] = None
  priority:Optional[int] = None
    
  @classmethod
  def from_vo(cls, todo_vo:TodoVO, id=None):
    return cls(
            id=todo_vo.id,
            title=todo_vo.title,
            notes=todo_vo.notes,
            updated=todo_vo.updated,
        )
    
  def fetch_evaluation(self):
    info = fetch_evaluation_todo(self.title)
    if info:
      self.difficulty = info["difficulty"]
      self.required_time = info["required_time"]
      self.priority = info["priority"]
    else:
      self.difficulty = None
      self.required_time = None
      self.priority = None
    print(f"info:{info}, title:{self.title}")
    return self
    
        
  def __str__(self):
    if self.difficulty:
      return f"title:{self.title}, required_time:{self.required_time}, difficulty:{self.difficulty}"
    else:
      return f"title:{self.title}, difficulty:{None}"