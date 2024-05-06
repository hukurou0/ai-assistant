from openai import OpenAI
from src.service.llm.gpt import tools
from dotenv import load_dotenv
import os

from src.repository.todo_repository import TodoRepository

from pydantic import BaseModel
from typing import Any

load_dotenv()

class GPT4EvaluationService(BaseModel):
  session:Any
  
  #TODO# titleのみで推論。プロンプトでlist名やnotesを混ぜたりなどで精度改善
  #TODO# Noneの時に再リクエス処理(回数制限やモデル変えるなど)
  async def evaluation_todo(self, todo, todo_list): # -> Todo
    content = f"以下のタスクのpriorityとdifficultyとrequired_timeを教えてください\n\
      タスク：{todo.title}"

    model = "gpt-4-turbo-preview"

    client = OpenAI(api_key=os.getenv("API_KEY"))

    response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content}],
                functions=tools.tools,
                tool_choice=None,
              )
    if response.choices[0].message.function_call:
      evaluation_params = eval(response.choices[0].message.function_call.arguments)
      todo.add_evaluation(evaluation_params)
      repository = TodoRepository(session=self.session)
      await repository.update_evaluation(todo)
    else:
      print(f"評価失敗「title:{todo.title}」")
    
  async def evaluation_todo_list(self, todo_list): # -> list[Todo]
      for todo in todo_list.todos:
        await self.evaluation_todo(todo, todo_list)
      return todo_list.todos
    
  async def fetch_complete_todos(self, todo_lists): # -> list[Todo]:
    all_complete_todos = []
    for todo_list in todo_lists:
      todos = await self.evaluation_todo_list(todo_list)
      all_complete_todos.extend(todos)
    return all_complete_todos
          