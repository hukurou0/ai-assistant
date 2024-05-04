from src.service.llm.gpt.evaluation import fetch_evaluation_task
from src.domain.vos.task import TaskVO

class Task():
  id:str
  title:str
  notes:str
  updated:str
  difficulty:int | None
  required_time:int | None
  priority:int | None
    
  def __init__(self, task_vo:TaskVO):
    self.id = task_vo.id
    self.title = task_vo.title
    self.notes = task_vo.notes
    self.updated = task_vo.updated
    
  @classmethod
  def from_vo(cls, task_vo:TaskVO, id=None):
    return cls(task_vo)
    
  def fetch_evaluation(self):
    info = fetch_evaluation_task(self.title)
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