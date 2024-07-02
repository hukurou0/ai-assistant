from src.domain.entities.free_time import FreeTime
from src.domain.entities.todo import Todo
from src.domain.vos.suggest_todo_vo import SuggestTodoVO


class SimpleAlgorithm:
    def __init__(self, free_time: FreeTime, todos: list[Todo]):
        self.free_time = free_time
        self.todos = todos

    def execute(self):
        well_todos: list[SuggestTodoVO] = []
        duration = self.free_time.get_duration()
        for i, todo in enumerate(self.todos):
            if todo.required_time:
                if duration >= todo.required_time:
                    well_todo = SuggestTodoVO(free_time=self.free_time, todo=todo)
                    well_todos.append(well_todo)
                    duration -= todo.required_time
                    del self.todos[i]
        return well_todos
