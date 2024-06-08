from pydantic import BaseModel
from typing import Union
from src.service.shared.component.todo.google_todo import GoogleTodoComponent
from src.service.shared.component.evaluation.gpt4o.gpt4o_evaluation import GPT4OEvaluationComponent
from src.service.shared.component.evaluation.gpt4.gpt4_evaluation import GPT4EvaluationComponent

class SyncTodoService(BaseModel):
  todo_component:Union[GoogleTodoComponent]
  evaluation_component:Union[GPT4EvaluationComponent, GPT4OEvaluationComponent]
  
  async def execute(self):
    await self.todo_component.fetch_todo_lists()
    await self.todo_component.do_import_to_local()
    await self.evaluation_component.do_evaluation()
    return "finished"
