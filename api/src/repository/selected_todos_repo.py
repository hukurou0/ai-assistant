from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import selectinload

from pydantic import BaseModel
from typing import Any
from src.models.todo_list_model import TodoModel
from src.repository.todo_list_repo import TodoMapper
from src.domain.entities.selected_todos import SelectedTodos
from src.domain.entities.selected_todo import SelectedTodo
from src.models.selected_todos import SelectedTodosModel

from datetime import datetime

class SelectedTodosMapper:
  """ @staticmethod
  def to_model(selected_todos_entity) -> SelectedTodosModel:
    return TodoListModel(todo_list_entity = todo_list_entity) """
  
  def to_entity(selected_todos_model:SelectedTodosModel, todos:list[SelectedTodo]) -> SelectedTodos:
    selected_todos = SelectedTodos(
      id    = selected_todos_model.id,
      date  = selected_todos_model.date,
      )
    todos = [SelectedTodoMapper.to_entity(todo, selected_todos_model.start, selected_todos_model.end) for todo in selected_todos_model.todo]
    selected_todos.set_todos(todos)
    return selected_todos

class SelectedTodoMapper:
  """ @staticmethod
  def to_model(todo_entity:Todo, todo_list_model:TodoListModel) -> TodoModel:
    return TodoModel(todo_entity = todo_entity, todo_list_model = todo_list_model) """
  @staticmethod
  def to_entity(todo:TodoModel, start:datetime, end:datetime) -> SelectedTodo:
    return SelectedTodo(
      id    = todo.id,
      todo  = TodoMapper.to_entity(todo),
      start = start,
      end   = end
    )

class SelectedTodosRepo(BaseModel):
  session:Any
  
  async def fetch_by_date(self, date:datetime) -> SelectedTodos | None: # 未テスト
    print("#4##########################################")
    print(date)
    print(type(date))
    stmt = select(SelectedTodosModel).where(SelectedTodosModel.date == date)
    result = await self.session.execute(stmt)
    print("#5##########################################")
    selected_todos_models = result.scalars().all()
    todos = [selected_todos_model.todo for selected_todos_model in selected_todos_models]
    if selected_todos_models:
      print("#6##########################################")
      return SelectedTodoMapper.to_entity(selected_todos_models[0], todos)
    else:
      return None
  
  async def get_today_selected_todos(self) -> SelectedTodos:
    print("#3##########################################")
    selected_todos = await self.fetch_by_date(date = datetime.now())
    if selected_todos:
      return SelectedTodosMapper.to_entity(selected_todos)
    else:
      return None
      
  async def save(self, selected_todos:SelectedTodos):
    if not(selected_todos.add_todos) and not(selected_todos.delete_todos):
      return
    
    for add_todo in selected_todos.add_todos:
      selected_todos = SelectedTodosModel(
        id    = selected_todos.id,
        date  = selected_todos.date,
        start = add_todo.start,
        end   = add_todo.end,
        todo  = add_todo
      )
      self.session.add(selected_todos)
      await self.session.commit()
    selected_todos.add_todos = []
    
    for delete_todo in selected_todos.delete_todos: # 未実装
      raise
      stmt = delete(SelectedTodosModel).where(SelectedTodosModel.id == selected_todos.id)
      selected_todos.delete_todos = []