from pydantic import BaseModel
from src.models.todo_model import TodoModel
from typing import Any

class TodoMapper:
	@staticmethod
	def to_model(todo_entity):
			return TodoModel(todo_entity=todo_entity)

class TodoRepository(BaseModel):
  session:Any
    
  async def create(self, todo_entity, batch=False):
    todo_model = TodoMapper.to_model(todo_entity)
    self.session.add(todo_model)
    if batch:
      return todo_model # コミットしない(with終了でトランザクション切れるときにコミット)
    else:
      await self.session.commit()