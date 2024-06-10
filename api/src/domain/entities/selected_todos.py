from pydantic import BaseModel
from typing import Optional
from src.domain.entities.selected_todo import SelectedTodo
from datetime import datetime


class SelectedTodos(BaseModel):
  id:str
  date:datetime
  _todos:Optional[list[SelectedTodo]] = []
  
  # 以下は実装上で必要な変数
  add_todos:Optional[list[SelectedTodo]] = []
  delete_todos:Optional[list[SelectedTodo]] = []
  
  def set_todos(self, todos:list[SelectedTodo]):
    self._todos = todos
  
  def get_todos(self):
    if self.add_todos or self.delete_todos:
      raise Exception('保存されていないaddまたはupdate、deleteがあります。repositoryで保存後todosにアクセスしてください')
    return self._todos
        
  def __str__(self):
    if self.add_todos or self.delete_todos:
      raise Exception('保存されていないaddまたはupdate、deleteがあります。repositoryで保存後printを実行してください')
    return f"date:{self.date}, todos:{self.get_todos()}"
  
  def add_todo(self, todo:SelectedTodo):
    self.add_todos.append(todo)
    
  def delete_todo(self, todo:SelectedTodo):
    self.delete_todos.append(todo)