from cloud.cloud_calendar.google_calendar import GoogleCalendar
from cloud.cloud_todo.google_todo import GoogleTodo

from entities.task import Task
from vo.todo_list import TodoListVO
  
  
calendar = GoogleCalendar()
calendar.get_events()
free_times = calendar.find_free_times()
for free_time in free_times:
  print(free_time)
  
todo = GoogleTodo()
todo_lists:list[TodoListVO] = todo.fetch_todo_lists()
complete_todo_list:list[Task] = []
for todo_list in todo_lists:
  complete_todo_list.extend([Task.from_vo(task).fetch_evaluation() for task in todo_list.tasks])
  #print(f"complete_todo_list:{complete_todo_list}")

for free_time in free_times:
  for i, complete_todo in enumerate(complete_todo_list):
    if complete_todo.required_time:
      if free_time.duration >= complete_todo.required_time:
        print(free_time)
        print(complete_todo)
        print()
        free_time.duration -= complete_todo.required_time
        del complete_todo_list[i]
  
