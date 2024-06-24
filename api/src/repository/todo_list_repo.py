from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload

from pydantic import BaseModel
from typing import Any
from src.models.todo_list_model import TodoListModel
from src.models.todo_list_model import TodoModel
from src.domain.entities.todo_list import TodoList
from src.domain.entities.todo import Todo
from src.domain.entities.user import User

class TodoListMapper:
  @staticmethod
  def to_model(todo_list_entity:TodoList, user:User) -> TodoListModel:
    return TodoListModel(todo_list_entity = todo_list_entity, user = user)
  
  def to_entity_without_todos(todo_list_model:TodoListModel) -> TodoList:
    return TodoList(
      id              = todo_list_model.id,
      title           = todo_list_model.title,
      updated         = todo_list_model.updated,
      last_evaluation = todo_list_model.last_evaluation,
      )
  def to_entity_with_todos(todo_list_model:TodoListModel, todo_models:list[TodoModel]) -> TodoList:
    todo_list = TodoList(
      id              = todo_list_model.id,
      title           = todo_list_model.title,
      updated         = todo_list_model.updated,
      last_evaluation = todo_list_model.last_evaluation,
      )
    todo_list.set_todos([TodoMapper.to_entity(todo_model) for todo_model in todo_models])
    return todo_list

class TodoMapper:
  @staticmethod
  def to_model(todo_entity:Todo, todo_list_model:TodoListModel) -> TodoModel:
    return TodoModel(todo_entity = todo_entity, todo_list_model = todo_list_model)
  @staticmethod
  def to_entity(todo_model:TodoModel) -> Todo:
    return Todo(
      id            = todo_model.id,
      title         = todo_model.title,
      notes         = todo_model.notes,
      updated       = todo_model.updated,
      position      = todo_model.position,
      status        = todo_model.status,
      due           = todo_model.due,
      difficulty    = todo_model.difficulty,
      required_time = todo_model.required_time,
      priority      = todo_model.priority,
      )

class TodoListRepo(BaseModel):
  session:Any
    
  async def fetch_user_lists_without_todos(self):
    pass
   
  async def fetch_list_by_todo_id(self, todo_id:str) -> TodoList | None:
    stmt = select(TodoListModel).join(TodoModel).where(TodoModel.id == todo_id).options(selectinload(TodoListModel.todos))
    result = await self.session.execute(stmt)
    todo_list_model = result.scalars().all()
    if todo_list_model:
      return TodoListMapper.to_entity_with_todos(todo_list_model[0], todo_list_model[0].todos)
    else:
      return None 
    
  async def fetch_user_lists_with_todos(self, user:User) -> list[TodoList]:
    stmt = select(TodoListModel).where(TodoListModel.user_id == user.id).options(selectinload(TodoListModel.todos))
    results = await self.session.execute(stmt)
    todo_list_models = results.scalars().all()  
    todo_list_entities = []
    for todo_list_model in todo_list_models:
      #print(todo_list_model) #TODO# todo_list_model.last_evaluationがなぜかNone
      todo_models = todo_list_model.todos
      todo_list_entity = TodoListMapper.to_entity_without_todos(todo_list_model)
      todo_entities = [TodoMapper.to_entity(todo_model) for todo_model in todo_models]
      todo_list_entity.set_todos(todo_entities)
      todo_list_entities.append(todo_list_entity)
    return todo_list_entities
  
  async def fetch_list_by_id(self, list_id:str) -> TodoList | None:
    stmt = select(TodoListModel).where(TodoListModel.id == list_id)
    result = await self.session.execute(stmt)
    todo_list_model = result.scalars().all()
    if todo_list_model:
      return TodoListMapper.to_entity_without_todos(todo_list_model[0])
    else:
      return None
  
  async def create_list(self):
    pass
  
  async def create_list_with_todos(self, todo_list_entity:TodoList, user:User):
    todo_list_model = TodoListMapper.to_model(todo_list_entity, user)
    print(f"todo_list_model:{todo_list_model}")
    self.session.add(todo_list_model)
    todo_entities = todo_list_entity.get_todos()
    for todo_entity in todo_entities:
      todo_model = TodoMapper.to_model(todo_entity, todo_list_model)
      self.session.add(todo_model)
    await self.session.commit()
  
  async def update_list(self, todo_list_entity:TodoList):
    # listのupdate
    stmt = update(TodoListModel).where(TodoListModel.id == todo_list_entity.id).values(
      title           = todo_list_entity.title,
      updated         = todo_list_entity.updated,
      last_evaluation = todo_list_entity.last_evaluation,
      )
    await self.session.execute(stmt)
    await self.session.commit()
    
    if not(todo_list_entity.add_todos) and not(todo_list_entity.update_todos) and not(todo_list_entity.delete_todos):
      return
    
    stmt = select(TodoListModel).where(TodoListModel.id == todo_list_entity.id)
    result = await self.session.execute(stmt)
    todo_list_model = result.scalars().one()
    
    # todoのcreate
    if todo_list_entity.add_todos:
      todos = todo_list_entity.add_todos
      for todo in todos:
        new_todo = TodoMapper.to_model(todo_entity=todo, todo_list_model=todo_list_model)
        self.session.add(new_todo)
        await self.session.commit()
      todo_list_entity.add_todos = []
      
    # todoのupdate
    if todo_list_entity.update_todos:
      todos = todo_list_entity.update_todos
      for todo in todos:
        #TODO" 全部updateだとオーバヘッド大きいかも。update_evaluationを別で用意するなどで無駄なupdateを減らした方がよい？
        stmt = update(TodoModel).where(TodoModel.id == todo.id).values(
          title         = todo.title,
          notes         = todo.notes,
          updated       = todo.updated,
          position      = todo.position,
          status        = todo.status,
          due           = todo.due,
          difficulty    = todo.difficulty,
          required_time = todo.required_time,
          priority      = todo.priority
          )
        await self.session.execute(stmt)
        await self.session.commit()
      
      todo_list_entity.update_todos = []
    
    # todoのdelete
    if todo_list_entity.delete_todos:
      raise
      todo_list_entity.delete_todos = []
    
  async def delete_list(self):
    pass