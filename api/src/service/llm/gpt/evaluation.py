from openai import OpenAI
from src.service.llm.gpt import tools
from dotenv import load_dotenv
import os

load_dotenv()

#TODO# titleのみで推論。プロンプトでlist名やnotesを混ぜたりなどで精度改善
#TODO# Noneの時に再リクエス処理(回数制限やモデル変えるなど)
def fetch_evaluation_todo(title: str) -> dict:
  content = f"以下のタスクのpriorityとdifficultyとrequired_timeを教えてください\n\
    タスク：{title}"

  model = "gpt-4-turbo-preview"

  client = OpenAI(api_key=os.getenv("API_KEY"))

  response = client.chat.completions.create(
              model=model,
              messages=[{"role": "user", "content": content}],
              functions=tools.tools,
              tool_choice=None,
            )
  if response.choices[0].message.function_call:
    evaluation_todo = response.choices[0].message.function_call.arguments
    return eval(evaluation_todo) # エラー処理必要
  else:
    print(f"title:{title}")
    return None

#todo = "年金を払う"
#print(fetch_evaluation_todo(todo)) 
        