from sqlalchemy.future import select

from pydantic import BaseModel
from typing import Any
from src.domain.entities.event import Event

from src.models.event_model import EventModel

from datetime import date, timedelta
import pytz

from src.util.handle_time import get_start_of_datetime


class EventMapper:
    @staticmethod
    def to_model(event_entity: Event, user_id: str) -> EventModel:
        return EventModel(
            id=event_entity.id,
            user_id=user_id,
            summary=event_entity.summary,
            description=event_entity.description,
            start=event_entity.start,
            end=event_entity.end,
        )

    @staticmethod
    def to_entity(event_model: EventModel) -> Event:
        tz_tokyo = pytz.timezone("Asia/Tokyo")
        return Event(
            id=event_model.id,
            summary=event_model.summary,
            description=event_model.description,
            start=event_model.start.astimezone(tz_tokyo),
            end=event_model.end.astimezone(tz_tokyo),
        )


class EventRepo(BaseModel):
    session: Any

    async def save(self, events: list[Event], user_id: str):
        event_models = [EventMapper.to_model(event, user_id) for event in events]
        self.session.add_all(event_models)
        await self.session.commit()

    async def fecth_by_date(self, target_date: date, user_id: str) -> list[Event]:
        start_of_day = get_start_of_datetime(target_date)
        end_of_day = start_of_day + timedelta(days=1)
        stmt = select(EventModel).where(
            EventModel.user_id == user_id,
            EventModel.start >= start_of_day,
            EventModel.end <= end_of_day,
        )
        result = await self.session.execute(stmt)
        event_models = result.scalars().all()
        if event_models:
            return [EventMapper.to_entity(event_model) for event_model in event_models]
        else:
            return []

    async def delete_by_date(self, target_date: date, user_id: str):
        start_of_day = get_start_of_datetime(target_date)
        end_of_day = start_of_day + timedelta(days=1)
        stmt = select(EventModel).where(
            EventModel.user_id == user_id,
            EventModel.start >= start_of_day,
            EventModel.end <= end_of_day,
        )
        result = await self.session.execute(stmt)
        event_models = result.scalars().all()
        for event_model in event_models:
            await self.session.delete(event_model)
        await self.session.commit()
