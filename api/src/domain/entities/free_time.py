from pydantic import BaseModel
from datetime import datetime

class FreeTime(BaseModel):
  id:str
  start:datetime
  end:datetime
  
        
  def __str__(self):
    return f"start:{self.start}, end:{self.end}"