from sqlalchemy.future import select

from src.models.free_time_model import FreeTimeModel

from pydantic import BaseModel
from typing import Any
from src.domain.entities.free_time import FreeTime

from datetime import date, timedelta
import pytz

from src.util.handle_time import get_start_of_datetime


class FreeTimeMapper:
    @staticmethod
    def to_model(free_time_entity: FreeTime, user_id: str) -> FreeTimeModel:
        return FreeTimeModel(
            id=free_time_entity.id,
            user_id=user_id,
            start=free_time_entity.start,
            end=free_time_entity.end,
        )

    def to_entity(free_time_model: FreeTimeModel) -> FreeTime:
        tz_tokyo = pytz.timezone("Asia/Tokyo")
        return FreeTime(
            id=free_time_model.id,
            start=free_time_model.start.astimezone(tz_tokyo),
            end=free_time_model.end.astimezone(tz_tokyo),
        )


class FreeTimeRepo(BaseModel):
    session: Any

    async def fetch_by_date(self, target_date: date, user_id: str) -> list[FreeTime]:
        start_of_day = get_start_of_datetime(target_date)
        end_of_day = start_of_day + timedelta(days=1)
        stmt = select(FreeTimeModel).where(
            FreeTimeModel.user_id == user_id,
            FreeTimeModel.start >= start_of_day,
            FreeTimeModel.end <= end_of_day,
        )
        result = await self.session.execute(stmt)
        free_time_models = result.scalars().all()
        if free_time_models:
            return [
                FreeTimeMapper.to_entity(free_time_model)
                for free_time_model in free_time_models
            ]
        else:
            return []

    async def save(self, free_times: list[FreeTime], user_id: str):
        for free_time in free_times:
            free_time_model = FreeTimeMapper.to_model(free_time, user_id)
            self.session.add(free_time_model)
        await self.session.commit()

    async def fetch_by_id(self, id: str) -> FreeTime:
        stmt = select(FreeTimeModel).where(FreeTimeModel.id == id)
        result = await self.session.execute(stmt)
        free_time_model = result.scalars().first()
        if free_time_model:
            return FreeTimeMapper.to_entity(free_time_model)
        else:
            return None

    async def delete_by_date(self, target_date: date, user_id: str):
        start_of_day = get_start_of_datetime(target_date)
        end_of_day = start_of_day + timedelta(days=1)
        stmt = select(FreeTimeModel).where(
            FreeTimeModel.user_id == user_id,
            FreeTimeModel.start >= start_of_day,
            FreeTimeModel.end <= end_of_day,
        )
        result = await self.session.execute(stmt)
        free_time_models = result.scalars().all()
        for free_time_model in free_time_models:
            await self.session.delete(free_time_model)
        await self.session.commit()
