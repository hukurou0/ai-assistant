from openai import OpenAI
from src.service.shared.provider.evaluation.gpt4omini import tools
from dotenv import load_dotenv
import os

from pydantic import BaseModel
from typing import Any
from src.domain.entities.todo import Todo
from src.domain.entities.todo import Todo
from src.domain.vos.evaluation_parms import EvaluationParmsVO

load_dotenv()


class GPT4OMiniEvaluationProvider(BaseModel):
    session: Any

    # TODO# Noneの時に再リクエス処理(回数制限やモデル変えるなど)
    async def evaluate(self, todo: Todo) -> Todo | None:
        content = f"Please let me know the REQUIRED_TIME, PRIORITY_LEVEL and IMPORTANCE_LEVEL for the following tasks.\n\
            If it is difficult to reason about REQUIRED_TIME, PRIORITY_LEVEL and IMPORTANCE_LEVEL, do not return anything.\n\
            TodoTitle:{todo.title}\n\
            TodoTags:{[tag.name for tag in todo.tags]}\n"

        if todo.notes:
            content += f"Notes:{todo.notes}\n"

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
            return todo
        else:
            print(f"評価失敗「title:{todo.title}」")
            return None
