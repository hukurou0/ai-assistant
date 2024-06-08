from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

from src.service.shared.utils.google_base import GoogleBase
from src.repository.todo_list_repo import TodoListRepo

from pydantic import BaseModel
from src.domain.entities.todo_list import TodoList
from src.domain.entities.todo import Todo
from typing import Any, Optional


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = 'postgresql://myuser:mypassword@postgres/mydatabase'

# エンジンの作成
engine = create_engine(database_url)

# セッションの作成
""" Session = sessionmaker(bind=engine)
session = Session() """

class GoogleTodoComponent(GoogleBase, BaseModel):
  session:Any
  todo_lists:Optional[list[TodoList]] = None
  
  async def _fetch_todo_lists(self)->list[TodoList]:
    creds = self.get_cred()

    try:
      service = build("tasks", "v1", credentials=creds)

      # Call the Tasks API
      results = service.tasklists().list(maxResults=10).execute()
      items = results.get("items", [])
      todo_lists = [
        TodoList(
          id = item["id"],
          title = item["title"],
          updated = datetime.datetime.fromisoformat(item["updated"][:-1] + '+00:00'),
        ) 
        for item in items
      ]
      return todo_lists
    except HttpError as err:
      print(err)
      return err
  
  async def _fetch_todos_from_todo_list(self, todo_list:TodoList)->TodoList:
    creds = self.get_cred()

    try:
      service = build("tasks", "v1", credentials=creds)

      # Call the Tasks API
      results = service.tasks().list(tasklist = todo_list.id).execute()
      items = results.get("items", [])
      todos = [
        Todo(
          id              = item["id"],
          title           = item["title"],
          updated         = item["updated"],
          position        = item["position"],
          status          = item["status"],
          due             = item.get("due",""),
          notes           = item.get("notes",""),
        )
        for item in items
      ]
      active_todos = [todo for todo in todos if todo.status != "completed"]
      
      todo_list.set_todos(active_todos)
      
    except HttpError as err:
      print(err)
      
    return todo_list
      
  async def fetch_todo_lists(self):
    todo_lists = await self._fetch_todo_lists()
    all_todo_lists:list[TodoList] = []
    for todo_list in todo_lists:
      todo_list_have_todos = await self._fetch_todos_from_todo_list(todo_list)
      all_todo_lists.append(todo_list_have_todos)
    self.todo_lists = all_todo_lists
    
  async def do_import_to_local(self):
    repo = TodoListRepo(session=self.session)
    for todo_list in self.todo_lists:
      if await repo.fetch_list_by_id(todo_list.id):
        await repo.update_list(todo_list)
      else:
        await repo.create_list_with_todos(todo_list)