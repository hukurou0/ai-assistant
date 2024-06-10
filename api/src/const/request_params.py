from pydantic import BaseModel

class SelectedTodoAddParams(BaseModel):
    todo_id: str
    free_time_id: str