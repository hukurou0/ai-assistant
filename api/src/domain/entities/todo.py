from src.service.llm.gpt.evaluation import fetch_evaluation_todo
from src.domain.vos.todo import TodoVO

class Todo():
  id:str
  title:str
  notes:str
  updated:str
  difficulty:int | None
  required_time:int | None
  priority:int | None
    
  def __init__(self, todo_vo:TodoVO):
    self.id = todo_vo.id
    self.title = todo_vo.title
    self.notes = todo_vo.notes
    self.updated = todo_vo.updated
    
  @classmethod
  def from_vo(cls, todo_vo:TodoVO, id=None):
    return cls(todo_vo)
    
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