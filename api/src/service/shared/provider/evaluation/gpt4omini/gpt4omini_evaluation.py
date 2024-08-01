from openai import OpenAI
from src.service.shared.provider.evaluation.gpt4omini import tools
from dotenv import load_dotenv
import os

from pydantic import BaseModel
from typing import Any
from src.domain.entities.todo_list import TodoList
from src.domain.entities.todo import Todo
from src.domain.vos.evaluation_parms import EvaluationParmsVO

load_dotenv()


class GPT4OMiniEvaluationProvider(BaseModel):
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

        model = "gpt-4o-mini-2024-07-18"

        client = OpenAI(api_key=os.getenv("API_KEY"))

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": content}],
            tools=tools.tools,
            tool_choice="auto",
        )
        if response.choices[0].message.tool_calls:
            evaluation_params = eval(
                response.choices[0].message.tool_calls[0].function.arguments
            )
            todo.add_evaluation(
                EvaluationParmsVO(
                    required_time=evaluation_params["required_time"],
                    priority_level=evaluation_params["priority_level"],
                    importance_level=evaluation_params["importance_level"],
                )
            )
            todo_list.update_todo(todo)
        else:
            print(f"評価失敗「title:{todo.title}」")

    async def evaluation_todo_in_list(self, todo_list: TodoList):
        for todo in todo_list.get_todos():
            await self.evaluation_todo(todo, todo_list)
