from src.service.shared.component.calendar.google_calendar import GoogleCalendarComponent
from src.service.shared.provider.local_todo import LocalTodoProvider

from typing import Union
from pydantic import BaseModel
from src.domain.vos.suggest_todo import SuggestTodoVO

class SuggestTodoService(BaseModel):
  calendar_component:Union[GoogleCalendarComponent]
  todo_provider:Union[LocalTodoProvider]

  async def find_well_todos(self) -> list[SuggestTodoVO]: 
    free_times = self.calendar_component.find_free_times()
    todos = await self.todo_provider.fetch_todos()

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
    
