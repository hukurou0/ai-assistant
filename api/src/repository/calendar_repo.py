from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import selectinload

from src.domain.entities.event import Event

from pydantic import BaseModel
from typing import Any

class CalendarRepo(BaseModel):
  session:Any
  
  async def get(self) -> list[Event]:
    pass