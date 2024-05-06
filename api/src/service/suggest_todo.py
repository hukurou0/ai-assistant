from src.service.calendar.cloud.google_calendar import GoogleCalendarService
from src.service.todo.cloud.google_todo import GoogleTodoService
from src.service.llm.gpt.evaluation import GPT4EvaluationService

from typing import Union
from pydantic import BaseModel
from src.domain.vos.suggest_todo import SuggestTodoVO

class SuggestTodoService(BaseModel):
  calendar_service:Union[GoogleCalendarService]
  todo_service:Union[GoogleTodoService]
  evaluation_service:Union[GPT4EvaluationService]

  async def find_well_todos(self): 
    print("find_well_todos_start") 
    free_times = self.calendar_service.find_free_times()
    print("get_free_times") 
    todo_lists = await self.todo_service.fetch_todo_lists()
    print("get_todo_list") 
    complete_todos = await self.evaluation_service.fetch_complete_todos(todo_lists)
    print("get_complete_todo") 

    well_todos:list[SuggestTodoVO] = []
    for free_time in free_times:
      duration = free_time.duration
      for i, complete_todo in enumerate(complete_todos):
        if complete_todo.required_time:
          if duration >= complete_todo.required_time:
            well_todo = SuggestTodoVO(
                            free_time=free_time,
                            todo=complete_todo
                        )
            well_todos.append(well_todo)
            duration -= complete_todo.required_time
            del complete_todos[i]
            
    return well_todos
    
