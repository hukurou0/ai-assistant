from pydantic import BaseModel
from typing import Any
from src.domain.entities.todo import Todo
from src.domain.entities.user import User

from src.repository.todo_list_repo import TodoListRepo


class LocalTodoProvider(BaseModel):
    session: Any

    async def fetch_todos(self, user: User) -> list[Todo]:
        repo = TodoListRepo(session=self.session)
        todo_lists = await repo.fetch_user_lists_with_todos(user)
        all_todos = []
        for todo_list in todo_lists:
            all_todos.extend(todo_list.get_todos())
        return all_todos

    async def fetch_todo_by_id(self, todo_id: str) -> Todo:
        repo = TodoListRepo(session=self.session)
        todo_list = await repo.fetch_list_by_todo_id(todo_id)
        for todo in todo_list.get_todos():
            if todo.id == todo_id:
                return todo
        return None
