from pydantic import BaseModel
from typing import Union
from src.service.todo.cloud.google_todo import GoogleTodoService
from src.service.llm.gpt.evaluation import GPT4EvaluationService

class SyncTodoService(BaseModel):
  todo_service:Union[GoogleTodoService]
  evaluation_service:Union[GPT4EvaluationService]
  
  async def execute(self):
    todo_lists = await self.todo_service.fetch_todo_lists()
    complete_todos = await self.evaluation_service.do_evaluation(todo_lists)
    return "success"
