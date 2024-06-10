from pydantic import BaseModel

class SelectedTodoAddParams(BaseModel):
    todo_id: str
    free_time_id: str
    
class SelectedTodoRemoveParams(BaseModel):
    todo_id: str
    free_time_id: str