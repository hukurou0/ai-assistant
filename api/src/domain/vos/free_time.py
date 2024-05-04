from datetime import datetime
from pydantic import BaseModel

class FreeTimeVO(BaseModel, frozen=True):
  duration:int
  start:datetime
  end:datetime
  
  def __str__(self):
    return f"Free {self.duration} minutes from {self.start} to {self.end}"