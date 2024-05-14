from openai import OpenAI
from src.service.evaluation.gpt4 import tools
from dotenv import load_dotenv
import os
import datetime

from src.repository.todo_list_repo import TodoListRepo

from pydantic import BaseModel
from typing import Any
from src.domain.entities.todo_list import TodoList
from src.domain.entities.todo import Todo
from src.domain.vos.evaluation_parms import EvaluationParmsVO

load_dotenv()

class GPT4EvaluationService(BaseModel):
  session:Any
  
  #TODO# Noneの時に再リクエス処理(回数制限やモデル変えるなど)
  async def evaluation_todo(self, todo:Todo, todo_list:TodoList):
    content = f"Please let me know the PRIORITY, DIFFICULTY and REQUIRED_TIME for the following tasks.\n\
      If it is difficult to reason about PRIORITY, DIFFICULTY and REQUIRED_TIME, do not return anything.\n\
      TodoListTitle:{todo_list.title}\n\
      TodoTitle:{todo.title}"
      
    if todo.notes:
      content += f"\n\
        Notes:{todo.notes}"

    model = "gpt-4-turbo-preview"

    client = OpenAI(api_key=os.getenv("API_KEY"))

    response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": content}],
                tools=tools.tools,
                tool_choice="auto",
              )
    if response.choices[0].message.tool_calls:
      evaluation_params = eval(response.choices[0].message.tool_calls[0].function.arguments)
      todo.add_evaluation(
        EvaluationParmsVO(
          difficulty    = evaluation_params["difficulty"],
          required_time = evaluation_params["required_time"],
          priority      = evaluation_params["priority"]
        )
      )
      todo_list.update_todo(todo)
    else:
      print(f"評価失敗「title:{todo.title}」")
    
  async def evaluation_todo_in_list(self, todo_list:TodoList):
    for todo in todo_list.get_todos():
      await self.evaluation_todo(todo, todo_list)
    
  #TODO# なぜかuser_todo_list.last_evaluationがDBにデータがあってもNoneになっている。そのため毎回新規作成が走る。修正必要
  async def do_evaluation(self):
    repo = TodoListRepo(session = self.session)
    user_todo_lists = await repo.fetch_user_lists_with_todos()
    for user_todo_list in user_todo_lists:
      if not user_todo_list.last_evaluation: 
        # 新規作成のリストだとNullになっているので評価
        print("新規作成")
        await self.evaluation_todo_in_list(user_todo_list)
        user_todo_list.last_evaluation = datetime.datetime.now(tz=datetime.timezone.utc)
        await repo.update_list(user_todo_list)
      elif user_todo_list.updated > user_todo_list.last_evaluation:
        # 内容に変更があるため再評価
        print("変更有",user_todo_list)
        await self.evaluation_todo_in_list(user_todo_list)
        user_todo_list.last_evaluation = datetime.datetime.now(tz=datetime.timezone.utc)
        await repo.update_list(user_todo_list)
      else:
        # 変更がないため評価しない
        print("変更なし",user_todo_list)
          