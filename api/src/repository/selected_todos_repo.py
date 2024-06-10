from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import joinedload

from pydantic import BaseModel
from typing import Any
from src.models.todo_list_model import TodoModel
from src.repository.todo_list_repo import TodoMapper
from src.domain.entities.selected_todos import SelectedTodos
from src.domain.entities.selected_todo import SelectedTodo
from src.models.selected_todos import SelectedTodosModel
from src.repository.free_time_repo import FreeTimeMapper

from datetime import datetime
import pytz

class SelectedTodosMapper:
  def to_entity(selected_todo_models:list[SelectedTodosModel]) -> SelectedTodos:
    selected_todos = SelectedTodos(
      id    = "dymmy",
      date  = selected_todo_models[0].date,
      )
    todos = []
    for selected_todo_model in selected_todo_models:
      selected_todo = SelectedTodo(
        id    = selected_todo_model.id,
        todo  = TodoMapper.to_entity(selected_todo_model.todo),
        free_time = FreeTimeMapper.to_entity(selected_todo_model.free_time),
      )
      todos.append(selected_todo)
    selected_todos.set_todos(todos)
    return selected_todos

class SelectedTodosRepo(BaseModel):
  session:Any
  
  async def fetch_by_date(self, date:datetime) -> SelectedTodos | None:
    stmt = (
      select(SelectedTodosModel)
      .where(SelectedTodosModel.date == date)
      .options(joinedload(SelectedTodosModel.todo),
               joinedload(SelectedTodosModel.free_time))
      )
    result = await self.session.execute(stmt)
    selected_todos_models = result.scalars().all()
    if selected_todos_models:
      return SelectedTodosMapper.to_entity(selected_todos_models)
    else:
      return None
  
  async def get_today_selected_todos(self) -> SelectedTodos:
    tz_tokyo = pytz.timezone('Asia/Tokyo')
    today_start = datetime.now(tz_tokyo).replace(hour=0, minute=0, second=0, microsecond=0)
    selected_todos = await self.fetch_by_date(date = today_start)
    if selected_todos:
      return await self.fetch_by_date(date = today_start)
    else:
      return None
    
  async def fetch_by_free_time_id(self, free_time_id:str) -> SelectedTodos:
    stmt = (
      select(SelectedTodosModel)
      .where(SelectedTodosModel.free_time_id == free_time_id)
      .options(joinedload(SelectedTodosModel.todo),
              joinedload(SelectedTodosModel.free_time))
    )
    result = await self.session.execute(stmt)
    selected_todos_models = result.scalars().all()
    if selected_todos_models:
      return SelectedTodosMapper.to_entity(selected_todos_models)
    else:
      return None
    
  async def fetch_by_free_time_id(self, free_time_id:str) -> SelectedTodos:
    stmt = (
      select(SelectedTodosModel)
      .where(SelectedTodosModel.free_time_id == free_time_id)
      .options(joinedload(SelectedTodosModel.todo),
              joinedload(SelectedTodosModel.free_time))
    )
    result = await self.session.execute(stmt)
    selected_todos_models = result.scalars().all()
    if selected_todos_models:
      return SelectedTodosMapper.to_entity(selected_todos_models)
    else:
      return None
      
  async def save(self, selected_todos:SelectedTodos):
    if not(selected_todos.add_todos) and not(selected_todos.delete_todos):
      return
    
    if selected_todos.add_todos:
      for add_todo in selected_todos.add_todos:
        selected_todo = SelectedTodosModel(
          id    = add_todo.id,
          date  = selected_todos.date,
          free_time_id = add_todo.free_time.id,
          todo_id  = add_todo.todo.id,
        )
        self.session.add(selected_todo)
        await self.session.commit()
      selected_todos.add_todos = []
    
    if selected_todos.delete_todos:
      for delete_todo in selected_todos.delete_todos:
        stmt = delete(SelectedTodosModel).where(SelectedTodosModel.id == delete_todo.id)
        await self.session.execute(stmt)
        await self.session.commit()
      selected_todos.delete_todos = []
        
  async def delete_todo_by_id(self, selected_todo_id:str):
    stmt = delete(SelectedTodosModel).where(SelectedTodosModel.id == selected_todo_id)
    await self.session.execute(stmt)
    await self.session.commit()
    return "success"