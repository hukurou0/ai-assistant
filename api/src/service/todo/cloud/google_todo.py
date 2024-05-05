from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.service.cloud.google_base import GoogleBase
from src.repository.todo_repository import TodoRepository

from pydantic import BaseModel
from src.domain.entities.todo_list import TodoList
from src.domain.entities.todo import Todo
from typing import Any


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url = 'postgresql://myuser:mypassword@postgres/mydatabase'

# エンジンの作成
engine = create_engine(database_url)

# セッションの作成
""" Session = sessionmaker(bind=engine)
session = Session() """

class GoogleTodoService(GoogleBase, BaseModel):
  session:Any
  
  async def fetch_todos_from_list_id(self, todo_list_id):
    creds = self.get_cred()

    try:
      service = build("tasks", "v1", credentials=creds)

      # Call the Tasks API
      results = service.tasks().list(tasklist = todo_list_id).execute()
      items = results.get("items", [])
      repository = TodoRepository(session=self.session)
      todos = [
        Todo(
          id=          item["id"],
          title=       item["title"],
          updated=     item["updated"],
          position=    item["position"],
          status=      item["status"],
          due=         item.get("due",""),
          notes=       item.get("notes",""),
          repository = repository
        )
        for item in items
      ]
      async with repository.session.begin():
        for todo in todos:
            await repository.create(todo, batch=True)
      return todos
    except HttpError as err:
      print(err)

  async def fetch_todo_lists(self)->list[TodoList]:
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
          updated = item["updated"],
          todos = await self.fetch_todos_from_list_id(item["id"])
        ) 
        for item in items
      ]
      return todo_lists
    except HttpError as err:
      print(err)
      return err
  