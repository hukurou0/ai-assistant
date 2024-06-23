from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

from src.repository.shared.google_base import GoogleBase

from pydantic import BaseModel
from src.domain.entities.todo_list import TodoList
from src.domain.entities.todo import Todo
from typing import Any, Optional

class GoogleTodoRepository(GoogleBase, BaseModel):
  session:Any
  
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
    return all_todo_lists