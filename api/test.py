from dataclasses import dataclass
from datetime import datetime

@dataclass()
class FreeTimeVO():
  duration:int
  start:datetime
  end:datetime
  
  def __str__(self):
    return f"Free {self.duration} minutes from {self.start} to {self.end}"

well_todo = {
            free_time:free_time.__str__(),
          }