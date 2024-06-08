from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import selectinload

from src.models.free_time_model import FreeTimeModel

from pydantic import BaseModel
from typing import Any
from src.domain.entities.free_time import FreeTime

from datetime import datetime

class FreeTimeMapper:
  @staticmethod
  def to_model(free_time_entity:FreeTime) -> FreeTimeModel:
    return FreeTimeModel(free_time_entity = free_time_entity)
  
  def to_entity(free_time_model:FreeTimeModel) -> FreeTime:
    return FreeTime(
      id    = free_time_model.id,
      start = free_time_model.start,
      end   = free_time_model.end,
      )

class FreeTimeRepo(BaseModel):
  session:Any
  
  