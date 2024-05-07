from pydantic import BaseModel
from src.models.todo_model import TodoModel
from src.domain.entities.todo import Todo
from sqlalchemy import update
from sqlalchemy.future import select
from typing import Any

class TodoMapper:
  @staticmethod
  def to_model(todo_entity, todo_list_id):
    return TodoModel(todo_entity=todo_entity, todo_list_id=todo_list_id)
  @staticmethod
  def to_entity(todo_model):
    return Todo(
      id=todo_model.id,
      title=todo_model.title,
      notes=todo_model.notes,
      updated=todo_model.updated,
      position=todo_model.position,
      status=todo_model.status,
      due=todo_model.due,
      difficulty=todo_model.difficulty,
      required_time=todo_model.required_time,
      priority=todo_model.priority,
      )

class TodoRepository(BaseModel):
  session:Any
    
  async def create(self, todo_entity, todo_list_id, batch=False):
    todo_model = TodoMapper.to_model(todo_entity, todo_list_id)
    self.session.add(todo_model)
    if batch:
      return todo_model # コミットしない(with終了でトランザクション切れるときにコミット)
    else:
      await self.session.commit()
      
  async def update_evaluation(self, todo_entity, batch=False):
    stmt = update(TodoModel).where(TodoModel.id == todo_entity.id).values(difficulty=todo_entity.difficulty,required_time=todo_entity.required_time,priority=todo_entity.priority)
    await self.session.execute(stmt)
    await self.session.commit()
    
  async def get_own_todos(self):
    query = select(TodoModel)
    result = await self.session.execute(query)
    todo_models = result.scalars().all()
    todo_entities = [TodoMapper.to_entity(todo_model) for todo_model in todo_models]
    return todo_entities