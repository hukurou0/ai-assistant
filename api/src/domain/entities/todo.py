from pydantic import BaseModel
from typing import Optional
from enum import Enum
from src.domain.vos.evaluation_parms import EvaluationParmsVO
from datetime import datetime
from src.domain.entities.user import User
from src.domain.entities.tag import Tag


class TodoStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "inProgress"
    COMPLETED = "completed"


class Todo(BaseModel):
    ## Original
    id: str
    user: User
    title: str
    notes: str
    status: TodoStatus
    due: Optional[datetime]
    tags: list[Tag]

    ## Evaluation
    required_time: Optional[int] = None
    priority_level: Optional[int] = None
    importance_level: Optional[int] = None

    ## Explanation of Evaluation Params
    class Explanation:
        required_time: str = (
            "\
      Number of minutes it takes to perform the task.\
      "
        )

        priority_level: str = (
            "\
      1-10 number of how quickly you should do that task.\n\
      For example, replying to an email or doing laundry should be done as soon as possible,\
      so it is more urgent, and sorting out unnecessary paperwork is less urgent\
      because it does not need to be done immediately.\
      "
        )

        importance_level: str = (
            "\
      1-10 number for the importance of that task.\n\
      For example, regular medical checkups and tax payments are highly important\
      because they must be done, while sorting out unnecessary emails and notifications\
      is less important because putting them off will not have a significant impact.\
      "
        )

    def add_evaluation(self, evaluation_params: EvaluationParmsVO):
        self.required_time = evaluation_params.required_time
        self.priority_level = evaluation_params.priority_level
        self.importance_level = evaluation_params.importance_level
        return self

    def __str__(self):
        if self.required_time:
            return f"title:{self.title}, required_time:{self.required_time}, priority_level:{self.priority_level}, importance_level:{self.importance_level}"
        else:
            return f"title:{self.title}, required_time:{None}"
