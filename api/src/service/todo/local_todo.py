from pydantic import BaseModel
from typing import Any
from src.domain.entities.todo import Todo

from src.repository.todo_list_repo import TodoListRepo

class LocalTodoService(BaseModel):
  session:Any
  
  async def fetch_todos(self) -> list[Todo]:
    repo = TodoListRepo(session=self.session)
    todo_lists = await repo.fetch_user_lists_with_todos()
    all_todos = []
    for todo_list in todo_lists:
      all_todos.extend(todo_list.get_todos())
    return all_todos