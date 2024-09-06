from pydantic import BaseModel
from typing import Any

from src.repository.google_todo_repo import GoogleTodoRepository
from src.repository.todo_repo import TodoRepo
from src.repository.user_repo import UserRepo
from src.domain.entities.todo import TodoStatus
from src.service.shared.provider.evaluation.gpt4omini.gpt4omini_evaluation import (
    GPT4OMiniEvaluationProvider,
)

from src.domain.entities.todo import Todo


class SyncTodoService(BaseModel):
    session: Any

    async def execute(self, user_id: str):
        # todoをすべて削除する
        todo_repo = TodoRepo(session=self.session)
        await todo_repo.delete_all_by_user_id(user_id)

        # Google TasksからTodoを取得し、DBに保存する
        user_repo = UserRepo(session=self.session)
        user = await user_repo.fetch_user_by_id(user_id)

        google_todo_repo = GoogleTodoRepository(session=self.session)
        todos = await google_todo_repo.fetch_todos(user)
        await todo_repo.batch_create(todos)

        # Todoの評価を行う
        todos = await todo_repo.fetch_todos_by_user(user)
        need_evaluation_todos = [
            todo
            for todo in todos
            if todo.status == TodoStatus.TODO and todo.required_time == None
        ]
        if need_evaluation_todos:
            evaluation_provider = GPT4OMiniEvaluationProvider(session=self.session)
            evaluated_todos: list[Todo] = []
            for todo in need_evaluation_todos:
                evaluated_todo = await evaluation_provider.evaluate(todo)
                if evaluated_todo:
                    evaluated_todos.append(evaluated_todo)

            await todo_repo.batch_updated(evaluated_todos)

        return "finished"
