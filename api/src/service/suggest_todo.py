from src.service.calendar.cloud.google_calendar import GoogleCalendarService
from src.service.todo.cloud.google_todo import GoogleTodoService

from typing import Union
from pydantic import BaseModel
from src.domain.entities.todo import Todo
from src.domain.vos.suggest_todo import SuggestTodoVO

class SuggestTodoService(BaseModel):
  calendar_service:Union[GoogleCalendarService]
  todo_service:Union[GoogleTodoService]

  def find_well_todos(self):  
    free_times = self.calendar_service.find_free_times()
    todo_lists = self.todo_service.fetch_todo_lists()

    complete_todo_list:list[Todo] = []
    for todo_list in todo_lists:
      complete_todo_list.extend([todo.fetch_evaluation() for todo in todo_list.todos])

    well_todos:list[SuggestTodoVO] = []
    for free_time in free_times:
      duration = free_time.duration
      for i, complete_todo in enumerate(complete_todo_list):
        if complete_todo.required_time:
          if duration >= complete_todo.required_time:
            well_todo = SuggestTodoVO(
                            free_time=free_time,
                            complete_todo=complete_todo
                        )
            well_todos.append(well_todo)
            duration -= complete_todo.required_time
            del complete_todo_list[i]
            
    return well_todos
    
