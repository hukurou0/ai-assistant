from src.service.calendar.cloud.google_calendar import GoogleCalendarService
from src.service.todo.local_todo import LocalTodoService

from typing import Union
from pydantic import BaseModel
from src.domain.vos.suggest_todo import SuggestTodoVO

class SuggestTodoService(BaseModel):
  calendar_service:Union[GoogleCalendarService]
  todo_service:Union[LocalTodoService]

  async def find_well_todos(self): 
    free_times = self.calendar_service.find_free_times()
    print(free_times)
    todos = await self.todo_service.fetch_todos()

    well_todos:list[SuggestTodoVO] = []
    for free_time in free_times:
      duration = free_time.duration
      for i, todo in enumerate(todos):
        if todo.required_time:
          if duration >= todo.required_time:
            well_todo = SuggestTodoVO(
                            free_time=free_time,
                            todo=todo
                        )
            well_todos.append(well_todo)
            duration -= todo.required_time
            del todos[i]
            
    return well_todos
    
