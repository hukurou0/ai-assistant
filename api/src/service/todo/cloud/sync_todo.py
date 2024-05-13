from pydantic import BaseModel
from typing import Union
from src.service.todo.cloud.google_todo import GoogleTodoService
from src.service.evaluation.gpt.gpt4_evaluation import GPT4EvaluationService

class SyncTodoService(BaseModel):
  todo_service:Union[GoogleTodoService]
  evaluation_service:Union[GPT4EvaluationService]
  
  async def execute(self):
    await self.todo_service.fetch_todo_lists()
    await self.todo_service.do_import_to_local()
    await self.evaluation_service.do_evaluation()
    return "finished"