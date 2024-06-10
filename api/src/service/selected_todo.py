from pydantic import BaseModel
from typing import Any

from src.domain.entities.todo import Todo
from src.domain.entities.selected_todos import SelectedTodos
from src.domain.entities.selected_todo import SelectedTodo

from src.service.shared.provider.local_todo import LocalTodoProvider
from src.repository.selected_todos_repo import SelectedTodosRepo
from src.repository.free_time_repo import FreeTimeRepo

from datetime import datetime
import pytz
from src.service.shared.utils.make_uuid import make_uuid


class SelectedTodosService(BaseModel):
  session:Any
  
  async def add_selected_todo_by_id(self, todo_id:str, free_time_id:str):
    todo: Todo = await LocalTodoProvider(session=self.session).fetch_todo_by_id(todo_id)
    select_todos_repo = SelectedTodosRepo(session = self.session)
    free_time_repo = FreeTimeRepo(session = self.session)
    selected_todos = await select_todos_repo.get_today_selected_todos()
    if not selected_todos:
      tz_tokyo = pytz.timezone('Asia/Tokyo')
      today_start = datetime.now(tz_tokyo).replace(hour=0, minute=0, second=0, microsecond=0)
      selected_todos = SelectedTodos(id = make_uuid(), date = today_start)
    free_time = await free_time_repo.fetch_by_id(free_time_id)
    selected_todo = SelectedTodo(id = make_uuid(), free_time = free_time, todo = todo)
    selected_todos.add_todo(selected_todo)
    await select_todos_repo.save(selected_todos)
    return "success"
  
  async def delete_selected_todo_by_id(self, todo_id:str, free_time_id:str):
    select_todos_repo = SelectedTodosRepo(session = self.session)
    selected_todos = await select_todos_repo.get_today_selected_todos()
    if selected_todos:
      for selected_todo in selected_todos.get_todos():
        if selected_todo.todo.id == todo_id and selected_todo.free_time.id == free_time_id:
          selected_todos.delete_todo(selected_todo)
          await select_todos_repo.save(selected_todos)
          return "success"
      return "Not Found SelectedTodo"
    else:
      return "Not Found SelectedTodos"