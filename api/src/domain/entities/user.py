from pydantic import BaseModel

class User(BaseModel):
  id:str
  email:str
  name:str
  picture_url:str
  access_token:str|None = None
  refresh_token:str|None = None
        
  def __str__(self):
    return f"User(id={self.id}, name={self.name})"