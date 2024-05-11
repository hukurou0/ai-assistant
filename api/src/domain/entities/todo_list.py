from pydantic import BaseModel
from src.domain.entities.todo import Todo
from typing import Optional
import datetime

class TodoList(BaseModel):
  id:str
  title:str
  updated:datetime.datetime
  last_evaluation:Optional[datetime.datetime] = None
  _todos:Optional[list[Todo]] = [] 
  
  # 以下は実装上で必要な変数
  add_todos:Optional[list[Todo]] = []
  update_todos:Optional[list[Todo]] = []
  delete_todos:Optional[list[Todo]] = []
  
  def set_todos(self, todos):
    self._todos = todos
  
  def get_todos(self):
    if self.add_todos or self.update_todos or self.delete_todos:
      raise Exception('保存されていないaddまたはupdate、deleteがあります。repositoryで保存後todosにアクセスしてください')
    return self._todos
  
  def __str__(self):
    return f"TodoList(id={self.id}, title={self.title}, updated={self.updated}, last_evaluation={self.last_evaluation})"
  
  def add_todo(self, todo):
    self.add_todos.append(todo)
    
  def update_todo(self, todo):
    self.update_todos.append(todo)
    
  def delete_todo(self, todo):
    self.delete_todos.append(todo)