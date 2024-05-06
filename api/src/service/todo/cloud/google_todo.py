from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.service.cloud.google_base import GoogleBase
from src.repository.todo_list_repository import TodoListRepository

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
          updated = item["updated"],
        ) 
        for item in items
      ]
      return todo_lists
    except HttpError as err:
      print(err)
      return err
  
  async def _fetch_todos_from_todo_list(self, todo_list:TodoList)->list[TodoList]:
    creds = self.get_cred()

    try:
      service = build("tasks", "v1", credentials=creds)

      # Call the Tasks API
      results = service.tasks().list(tasklist = todo_list.id).execute()
      items = results.get("items", [])
      todos = [
        Todo(
          id=          item["id"],
          title=       item["title"],
          updated=     item["updated"],
          position=    item["position"],
          status=      item["status"],
          due=         item.get("due",""),
          notes=       item.get("notes",""),
        )
        for item in items
      ]
      
      todo_list.todos = todos
      
      repository = TodoListRepository(session=self.session)
      async with repository.session.begin():
        await repository.create(todo_list)
      
    except HttpError as err:
      print(err)
      
    return todo_list
      
  async def fetch_todos(self):
    todo_lists = await self._fetch_todo_lists()
    all_todos = []
    for todo_list in todo_lists:
      todos = await self._fetch_todos_from_todo_list(todo_list)
      all_todos.extend(todos)
    return all_todos
  
#complete_todos:list[Todo] = [todo.fetch_evaluation() for todo in todos]