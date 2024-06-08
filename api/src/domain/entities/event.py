from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
  id:str
  title:str
  note:str
  start:datetime
  end:datetime
        
  def __str__(self):
    return f"title:{self.title}, start:{self.start}, end:{self.end}"