from pydantic import BaseModel


class EvaluationParmsVO(BaseModel):
    required_time: int
    priority_level: int
    importance_level: int

    def __str__(self):
        return f"required_time:{self.required_time}, priority_level:{self.priority_level}, importance_level:{self.importance_level}"
