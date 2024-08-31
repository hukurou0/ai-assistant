from pydantic import BaseModel
from src.domain.entities.user import User


class Tag(BaseModel):
    id: str
    name: str
    user: User

    def __str__(self):
        return f"Tag(id={self.id}, name={self.name})"
