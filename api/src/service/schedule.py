from pydantic import BaseModel
from typing import Any
from src.domain.entities.event import Event
from src.domain.entities.schedule import Schedule
from src.domain.entities.free_time import FreeTime
from src.domain.entities.user import User

from src.repository.google_calendar_repo import GoogleCalendarRepo
from src.repository.event_repo import EventRepo
from src.repository.free_time_repo import FreeTimeRepo
from src.repository.user_repo import UserRepo

from src.service.shared.utils.make_uuid import make_uuid

from datetime import datetime, timedelta
import pytz
from src.util.handle_time import get_today_date


class ScheduleService(BaseModel):
    session: Any

    # TODO# min_durationを設定できるように
    async def _find_free_time(
        self,
        events: list[Event],
        min_duration: int = 15,
        start_time: int = 7,
        end_time: int = 20,
    ) -> list[FreeTime]:
        free_times: list[FreeTime] = []
        tz_tokyo = pytz.timezone("Asia/Tokyo")
        now = datetime.now(tz_tokyo)
        # TODO# 終了時間調整できるように
        end = now.replace(hour=end_time, minute=0, second=0, microsecond=0)

        # 現在時刻がend_timeを過ぎている場合は、次の日のstart_timeからend_timeの中でfind_free_time
        if now > end:
            now = (now + timedelta(days=1)).replace(
                hour=start_time, minute=0, second=0, microsecond=0
            )
            end += timedelta(days=1)
        else:
            now = now.replace(hour=start_time, minute=0, second=0, microsecond=0)
        start_of_free_time = now

        for event in events:
            start_of_event = event.start
            if start_of_free_time < start_of_event:
                duration = (start_of_event - start_of_free_time).total_seconds() / 60
                if duration >= min_duration:
                    free_times.append(
                        FreeTime(
                            id=make_uuid(), start=start_of_free_time, end=start_of_event
                        )
                    )
            end_of_event = event.end
            start_of_free_time = max(start_of_free_time, end_of_event)

        # 最後のイベント後の空き時間も追加
        duration = (end - start_of_free_time).total_seconds() / 60
        if duration >= min_duration:
            free_times.append(
                FreeTime(id=make_uuid(), start=start_of_free_time, end=end)
            )

        return free_times

    async def sync(self, user: User):
        google_calendar_repo = GoogleCalendarRepo(session=self.session)
        event_repo = EventRepo(session=self.session)
        free_time_repo = FreeTimeRepo(session=self.session)
        events = await google_calendar_repo.get(user)
        await event_repo.save(events, user_id=user.id)
        free_times = await self._find_free_time(events)
        await free_time_repo.save(free_times, user_id=user.id)

    async def get_today(self, user_id: str, need_sync: bool) -> Schedule:
        today_date = get_today_date()
        event_repo = EventRepo(session=self.session)
        free_time_repo = FreeTimeRepo(session=self.session)

        if need_sync:
            await free_time_repo.delete_by_date(today_date, user_id)
            await event_repo.delete_by_date(today_date, user_id)
            user_repo = UserRepo(session=self.session)
            user = await user_repo.fetch_user_by_id(user_id)
            await self.sync(user)

        events = await event_repo.fecth_by_date(today_date, user_id)
        free_times = await free_time_repo.fetch_by_date(today_date, user_id)

        # イベントも空き時間もない場合は、一度も同期されていないので同期して再取得
        # メモ # バグの原因となる可能性があるコード
        if not (events) and not (free_times):
            user_repo = UserRepo(session=self.session)
            user = await user_repo.fetch_user_by_id(user_id)
            await self.sync(user)
            events = await event_repo.fecth_by_date(today_date, user_id)
            free_times = await free_time_repo.fetch_by_date(today_date, user_id)

        schedule = Schedule(id="dumy", events=events, free_times=free_times)
        return schedule
