from dataclasses import dataclass
from vo.task import TaskVO

@dataclass(frozen=True)
class TodoListVO():
  id:str
  title:str
  updated:str
  tasks:list[TaskVO]
  