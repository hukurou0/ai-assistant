from pydantic import BaseModel
from src.models.todo_list_model import TodoListModel
from src.models.todo_model import TodoModel
from src.repository.todo_repository import TodoRepository, TodoMapper
from src.domain.entities.todo_list import TodoList
from typing import Any
from sqlalchemy.future import select
from sqlalchemy import update

class TodoListMapper:
  @staticmethod
  def to_model(todo_list_entity):
    return TodoListModel(todo_list_entity=todo_list_entity)
  
  def to_entity(todo_list_model,todos=None):
    return TodoList(id=todo_list_model.id,title=todo_list_model.title,updated=todo_list_model.updated,last_evaluation=todo_list_model.last_evaluation, todos=todos)


class TodoListRepository(BaseModel):
  session:Any
    
  async def save(self, todo_list_entity):
    todo_list = await self.session.get(TodoListModel, todo_list_entity.id)
    if todo_list:
      pass
    else:
      todo_list_model = TodoListMapper.to_model(todo_list_entity)
      self.session.add(todo_list_model)
    
    stmt = select(TodoModel).where(TodoModel.todo_list_id == todo_list_entity.id)
    results = await self.session.execute(stmt)
    saved_todos = results.scalars().all()
    saved_todo_ids = {todo.id for todo in saved_todos} 
    fetch_todo_ids = {todo.id for todo in todo_list_entity.todos}
    new_todo_ids = fetch_todo_ids.difference(saved_todo_ids)
    
    #TODO# todoが更新された時、DBに反映、evaluationの実行をする
    if new_todo_ids:
      todo_repo = TodoRepository(session = self.session)
      new_todos = [todo for todo in todo_list_entity.todos if todo.id in new_todo_ids]
      for todo in new_todos:
        await todo_repo.create(todo, todo_list_id=todo_list_entity.id ,batch=True)
        
      await self.session.commit()
    else:
      pass
  
  async def get(self, todo_list_entity):
    todo_list_model = await self.session.get(TodoListModel, todo_list_entity.id)
    stmt = select(TodoModel).where(TodoModel.todo_list_id == todo_list_entity.id)
    results = await self.session.execute(stmt)
    todo_models = results.scalars().all()
    todo_entities = [TodoMapper.to_entity(todo_model) for todo_model in todo_models]
    if todo_list_model:
      todo_list_entity = TodoListMapper.to_entity(todo_list_model,todo_entities)
      return todo_list_entity
    else:
      return None
  
  async def update_last_evaluation(self, todo_list_entity):
    stmt = update(TodoListModel).where(TodoListModel.id == todo_list_entity.id).values(last_evaluation=todo_list_entity.last_evaluation)
    await self.session.execute(stmt)
    await self.session.commit()
    
  async def fetch_user_todo_lists(self):
    user_todo_lists = []
    
    stmt = select(TodoListModel)
    results = await self.session.execute(stmt)
    todo_list_models = results.scalars().all()
    for todo_list_model in todo_list_models:
      stmt = select(TodoModel).where(TodoModel.todo_list_id == todo_list_model.id)
      results = await self.session.execute(stmt)
      todo_models = results.scalars().all()
      todo_entities = [TodoMapper.to_entity(todo_model) for todo_model in todo_models]
      todo_list_entity = TodoListMapper.to_entity(todo_list_model,todo_entities)
      user_todo_lists.append(todo_list_entity)
      
    return user_todo_lists
    