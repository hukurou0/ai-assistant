from pydantic import BaseModel
from datetime import datetime


class FreeTime(BaseModel):
    id: str
    start: datetime
    end: datetime

    def get_duration(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)

    def __str__(self):
        return f"start:{self.start}, end:{self.end}"
