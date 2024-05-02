from cloud.cloud_calendar.google_calendar import GoogleCalendar
from cloud.cloud_todo.google_todo import GoogleTodo

from entities.task import Task
from vo.todo_list import TodoListVO
  

def find_well_todos():  
  calendar = GoogleCalendar()
  calendar.get_events()
  free_times = calendar.find_free_times()
  
  todo = GoogleTodo()
  todo_lists:list[TodoListVO] = todo.fetch_todo_lists()
  complete_todo_list:list[Task] = []
  for todo_list in todo_lists:
    complete_todo_list.extend([Task.from_vo(task).fetch_evaluation() for task in todo_list.tasks])

  well_todos = []
  for free_time in free_times:
    for i, complete_todo in enumerate(complete_todo_list):
      if complete_todo.required_time:
        if free_time.duration >= complete_todo.required_time:
          well_todo = {
            "free_time":free_time.__str__(),
            "complete_todo":complete_todo.__str__()
          }
          well_todos.append(well_todo)
          free_time.duration -= complete_todo.required_time
          del complete_todo_list[i]
          
  return well_todos
  
