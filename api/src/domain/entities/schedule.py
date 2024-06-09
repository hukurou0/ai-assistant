from pydantic import BaseModel
from src.domain.entities.free_time import FreeTime
from src.domain.entities.event import Event


class Schedule(BaseModel):
  id:str
  events:list[Event]
  free_times:list[FreeTime]
  
  def get_elements_sorted_by_time(self):
    elements = self.events + self.free_times
    return sorted(elements, key=lambda x: x.start)
        
  def __str__(self):
    return f"id:{self.id}, event数:{len(self.events)}, free_time数:{len(self.free_times)}"