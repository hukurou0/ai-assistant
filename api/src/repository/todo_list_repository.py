from pydantic import BaseModel
from src.models.todo_list_model import TodoListModel
from src.repository.todo_repository import TodoRepository
from typing import Any

class TodoListMapper:
	@staticmethod
	def to_model(todo_list_entity):
			return TodoListModel(todo_list_entity=todo_list_entity)

class TodoListRepository(BaseModel):
  session:Any
    
  async def create(self, todo_list_entity):
    todo_list_model = TodoListMapper.to_model(todo_list_entity)
    self.session.add(todo_list_model)
    
    todo_repo = TodoRepository(session = self.session)
    todos = todo_list_entity.todos
    for todo in todos:
      await todo_repo.create(todo, todo_list_id=todo_list_entity.id ,batch=True)
      
    await self.session.commit()