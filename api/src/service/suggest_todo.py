from typing import TypedDict
from src.domain.entities.todo import Todo
from src.domain.vos.free_time import FreeTimeVO
  
class WellTodo(TypedDict):
    free_time: FreeTimeVO
    complete_todo: Todo

class SuggestTodoService():
  def __init__(self, calendar_service, todo_service):
    self.calendar_service = calendar_service
    self.todo_service = todo_service

  def find_well_todos(self):  
    free_times = self.calendar_service.find_free_times()
    todo_lists = self.todo_service.fetch_todo_lists()

    complete_todo_list:list[Todo] = []
    for todo_list in todo_lists:
      complete_todo_list.extend([Todo.from_vo(todo).fetch_evaluation() for todo in todo_list.todos])

    well_todos:list[WellTodo] = []
    for free_time in free_times:
      for i, complete_todo in enumerate(complete_todo_list):
        if complete_todo.required_time:
          if free_time.duration >= complete_todo.required_time:
            well_todo = {
              "free_time":free_time,
              "complete_todo":complete_todo
            }
            well_todos.append(well_todo)
            free_time.duration -= complete_todo.required_time
            del complete_todo_list[i]
            
    return well_todos
    
