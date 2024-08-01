from dotenv import load_dotenv

from pydantic import BaseModel
from typing import Any
from src.domain.entities.todo_list import TodoList
from src.domain.entities.todo import Todo
from src.domain.vos.evaluation_parms import EvaluationParmsVO
import requests

load_dotenv()


class LocalOllama3EvaluationProvider(BaseModel):
    session: Any

    # TODO# Noneの時に再リクエス処理(回数制限やモデル変えるなど)
    async def evaluation_todo(self, todo: Todo, todo_list: TodoList):
        content = f"Please let me know the REQUIRED_TIME, PRIORITY_LEVEL and IMPORTANCE_LEVEL for the following tasks.\n\
      If it is difficult to reason about REQUIRED_TIME, PRIORITY_LEVEL and IMPORTANCE_LEVEL, do not return anything.\n\
      TodoListTitle:{todo_list.title}\n\
      TodoTitle:{todo.title}"

        if todo.notes:
            content += f"\n\
        Notes:{todo.notes}"

        response = requests.post(
            "http://ollama:9000/local_evaluate",
            json={"todo_id": todo.id, "content": content},
        )

        evaluated_params = response.json()

        todo.add_evaluation(
            EvaluationParmsVO(
                required_time=evaluated_params["required_time"],
                priority_level=evaluated_params["priority_level"],
                importance_level=evaluated_params["importance_level"],
            )
        )
        todo_list.update_todo(todo)

    async def evaluation_todo_in_list(self, todo_list: TodoList):
        for todo in todo_list.get_todos():
            await self.evaluation_todo(todo, todo_list)
