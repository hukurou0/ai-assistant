from pydantic import BaseModel
from src.domain.entities.free_time import FreeTime
from src.domain.entities.event import Event


class Schedule(BaseModel):
  id:str
  events:list[Event]
  free_times:list[FreeTime]
        
  def __str__(self):
    return f"id:{self.id}, event数:{len(self.events)}, free_time数:{len(self.free_times)}"