from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
  id:str
  summary:str
  description:str
  start:datetime
  end:datetime
        
  def __str__(self):
    return f"title:{self.summary}, start:{self.start}, end:{self.end}"