from pydantic import BaseModel

class EvaluationParmsVO(BaseModel, frozen=True):
  difficulty:int
  required_time:int
  priority:int
  
  def __str__(self):
    return f"difficulty:{self.difficulty}, required_time:{self.required_time}, priority:{self.priority}"