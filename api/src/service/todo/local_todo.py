from pydantic import BaseModel
from typing import Any

from src.repository.todo_repository import TodoRepository

class LocalTodoService(BaseModel):
  session:Any
  
  async def fetch_todos(self):
    repo = TodoRepository(session=self.session)
    todos = await repo.get_own_todos()
    return todos