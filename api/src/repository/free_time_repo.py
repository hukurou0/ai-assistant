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
    return FreeTimeModel(
      id    = free_time_entity.id,
      start = free_time_entity.start,
      end   = free_time_entity.end,
    )
  
  def to_entity(free_time_model:FreeTimeModel) -> FreeTime:
    return FreeTime(
      id    = free_time_model.id,
      start = free_time_model.start,
      end   = free_time_model.end,
      )

class FreeTimeRepo(BaseModel):
  session:Any
  
  async def fetch(self)-> list[FreeTime]:
    stmt = select(FreeTimeModel).where(FreeTimeModel.start >= datetime.now())
    result = await self.session.execute(stmt)
    free_time_models = result.scalars().all()
    if free_time_models:
      return [FreeTimeMapper.to_entity(free_time_model) for free_time_model in free_time_models]
    else:
      return None 
    
  async def save(self, free_times:list[FreeTime]):
    for free_time in free_times:
      free_time_model = FreeTimeMapper.to_model(free_time)
      self.session.add(free_time_model)
    await self.session.commit()