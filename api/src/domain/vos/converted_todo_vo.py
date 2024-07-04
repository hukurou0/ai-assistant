from pydantic import BaseModel


class ConvertedTodoVO(BaseModel):
    id: str
    value: float
    time: int

    def __str__(self):
        return f"id: {self.id}, value: {self.value}, time: {self.time}"
