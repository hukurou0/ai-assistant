from openai import OpenAI
from src.service.evaluation.gpt import tools
from dotenv import load_dotenv
import os
import datetime

from src.repository.todo_repository import TodoRepository
from src.repository.todo_list_repository import TodoListRepository

from pydantic import BaseModel
from typing import Any

load_dotenv()

class GPT4EvaluationService(BaseModel):
  session:Any
  
  #TODO# titleのみで推論。プロンプトでlist名やnotesを混ぜたりなどで精度改善
  #TODO# Noneの時に再リクエス処理(回数制限やモデル変えるなど)
  async def evaluation_todo(self, todo, todo_list): # -> Todo
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
    if response.choices[0].message.tool_calls[0].function:
      evaluation_params = eval(response.choices[0].message.tool_calls[0].function.arguments)
      todo.add_evaluation(evaluation_params)
      repository = TodoRepository(session=self.session)
      await repository.update_evaluation(todo)
    else:
      print(f"評価失敗「title:{todo.title}」")
    
  async def evaluation_todo_list(self, todo_list): # -> list[Todo]
      for todo in todo_list.todos:
        await self.evaluation_todo(todo, todo_list)
      return todo_list.todos
    
  async def do_evaluation(self, fetch_todo_lists): # -> list[Todo]:
    all_complete_todos = []
    repo = TodoListRepository(session = self.session)
    for fetch_todo_list in fetch_todo_lists:
      last_todo_list = await repo.get(fetch_todo_list)
      if last_todo_list.last_evaluation: # 新規作成のリストだとNullになっているので評価
        last_evaluation_time = last_todo_list.last_evaluation
        if fetch_todo_list.updated > last_evaluation_time:
          # 内容に変更があるため再評価
          print("変更有",fetch_todo_list)
          todos = await self.evaluation_todo_list(fetch_todo_list)
          all_complete_todos.extend(todos)
          fetch_todo_list.last_evaluation = datetime.datetime.now()
          await repo.update_last_evaluation(fetch_todo_list)
        else:
          # 変更がないため評価しない
          print("変更なし",fetch_todo_list)
          if last_todo_list.todos:
            todos = last_todo_list.todos
            all_complete_todos.extend(todos)
      else:
        # 新規のリストのtodoを評価
        print("新規作成")
        todos = await self.evaluation_todo_list(fetch_todo_list)
        all_complete_todos.extend(todos)
        fetch_todo_list.last_evaluation = datetime.datetime.now()
        await repo.update_last_evaluation(fetch_todo_list)
    return all_complete_todos
          