from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.service.cloud.google_base import GoogleBase

from pydantic import BaseModel
from src.domain.vos.todo_list import TodoListVO
from src.domain.vos.todo import TodoVO

class GoogleTodoService(GoogleBase, BaseModel):
  def fetch_todos_from_list_id(self, todo_list_id):
    creds = self.get_cred()

    try:
      service = build("tasks", "v1", credentials=creds)

      # Call the Tasks API
      results = service.tasks().list(tasklist = todo_list_id).execute()
      items = results.get("items", [])
      todos = [
        TodoVO(
          id=item["id"],
          title=item["title"],
          updated=item["updated"],
          position=item["position"],
          status=item["status"],
          due=item.get("due",""),
          notes=item.get("notes",""),
        )
        for item in items
      ]
      return todos
    except HttpError as err:
      print(err)

  def fetch_todo_lists(self)->list[TodoListVO]:
    creds = self.get_cred()

    try:
      service = build("tasks", "v1", credentials=creds)

      # Call the Tasks API
      results = service.tasklists().list(maxResults=10).execute()
      items = results.get("items", [])
      todo_lists = [
        TodoListVO(
          id = item["id"],
          title = item["title"],
          updated = item["updated"],
          todos = self.fetch_todos_from_list_id(item["id"])
        ) 
        for item in items
      ]
      return todo_lists
    except HttpError as err:
      print(err)
      return err
  