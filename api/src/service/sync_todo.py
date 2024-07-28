from pydantic import BaseModel
from typing import Any

from src.repository.google_todo_repo import GoogleTodoRepository
from src.repository.todo_list_repo import TodoListRepo
from src.repository.user_repo import UserRepo
from src.service.shared.provider.evaluation.gpt4o.gpt4o_evaluation import (
    GPT4OEvaluationProvider,
)
from src.service.shared.provider.evaluation.local.llama3.evaluation import (
    LocalOllama3EvaluationProvider,
)

import datetime


class SyncTodoService(BaseModel):
    session: Any

    async def execute(self, user_id: str):
        user_repo = UserRepo(session=self.session)
        user = await user_repo.fetch_user_by_id(user_id)

        google_todo_repo = GoogleTodoRepository(session=self.session)
        todo_lists = await google_todo_repo.fetch_todo_lists(user)

        todo_list_repo = TodoListRepo(session=self.session)
        for todo_list in todo_lists:
            if await todo_list_repo.fetch_list_by_id(todo_list.id):
                await todo_list_repo.update_list(todo_list)
            else:
                await todo_list_repo.create_list_with_todos(todo_list, user)
        user_todo_lists = await todo_list_repo.fetch_user_lists_with_todos(user)
        # TODO# なぜかuser_todo_list.last_evaluationがDBにデータがあってもNoneになっている。そのため毎回新規作成が走る。修正必要
        for user_todo_list in user_todo_lists:
            # 評価実行-新規作成のリスト
            if not user_todo_list.last_evaluation:
                await LocalOllama3EvaluationProvider(
                    session=self.session
                ).evaluation_todo_in_list(user_todo_list)
                user_todo_list.last_evaluation = datetime.datetime.now(
                    tz=datetime.timezone.utc
                )
                await todo_list_repo.update_list(user_todo_list)
            # 評価実行-todoの内容に変更があり
            elif user_todo_list.updated > user_todo_list.last_evaluation:
                await LocalOllama3EvaluationProvider(
                    session=self.session
                ).evaluation_todo_in_list(user_todo_list)
                user_todo_list.last_evaluation = datetime.datetime.now(
                    tz=datetime.timezone.utc
                )
                await todo_list_repo.update_list(user_todo_list)
            # 再評価の必要なし
            else:
                pass

        return "finished"
