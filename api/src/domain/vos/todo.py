from pydantic import BaseModel

class TodoVO(BaseModel, frozen=True):
  id:str
  title:str
  updated:str
  position: str
  status: str
  due: str
  notes:str