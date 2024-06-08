from pydantic import BaseModel
from typing import Any

from src.domain.entities.todo import Todo
from src.domain.entities.selected_todos import SelectedTodos
from src.domain.entities.selected_todo import SelectedTodo
from src.domain.vos.free_time import FreeTimeVO

from src.service.shared.provider.local_todo import LocalTodoProvider
from src.repository.selected_todos_repo import SelectedTodosRepo

from datetime import datetime
from src.service.shared.utils.make_uuid import make_uuid


class SelectedTodosService(BaseModel):
  session:Any
  
  async def add_selected_todo_by_id(self, todo_id:str, free_time:FreeTimeVO):
    todo: Todo = await LocalTodoProvider(session=self.session).fetch_todo_by_id(todo_id)
    repo = SelectedTodosRepo(session = self.session)
    selected_todos = await repo.get_today_selected_todos()
    if not selected_todos:
      selected_todos = SelectedTodos(id = make_uuid(), date = datetime.now())
    selected_todo = SelectedTodo(id = make_uuid(), start = free_time.start, end = free_time.end, todo = todo)
    selected_todos.add_todo(selected_todo)
    await repo.save(selected_todos)
    return "success"