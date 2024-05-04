from dataclasses import dataclass

@dataclass()
class TodoVO():
  id:str
  title:str
  updated:str
  position: str
  status: str
  due: str
  notes:str