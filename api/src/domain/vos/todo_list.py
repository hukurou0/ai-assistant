from dataclasses import dataclass
from src.domain.vos.todo import TodoVO

@dataclass(frozen=True)
class TodoListVO():
  id:str
  title:str
  updated:str
  todos:list[TodoVO]
  