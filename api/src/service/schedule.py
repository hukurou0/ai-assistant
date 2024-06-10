from pydantic import BaseModel
from typing import Any
from src.repository.calendar_repo import CalendarRepo
from src.repository.free_time_repo import FreeTimeRepo
from src.domain.entities.event import Event

from src.domain.entities.schedule import Schedule
from src.domain.entities.free_time import FreeTime

from src.service.shared.utils.make_uuid import make_uuid

from datetime import datetime, timedelta
import pytz

class ScheduleService(BaseModel):
  session:Any
  
  async def _find_free_time(self, events:list[Event], min_duration:int = 15, start_time:int = 7, end_time:int = 20) -> list[FreeTime]:   
    free_times:list[FreeTime] = []
    tz_tokyo = pytz.timezone('Asia/Tokyo')
    now = datetime.now(tz_tokyo)
    #TODO# 終了時間調整できるように
    end = now.replace(hour=end_time, minute=0, second=0, microsecond=0)
    
    # 現在時刻がend_timeを過ぎている場合は、次の日のstart_timeからend_timeの中でfind_free_time
    if now > end:
      now = (now + timedelta(days=1)).replace(hour=start_time, minute=0, second=0, microsecond=0)
      end += timedelta(days=1)
    start_of_free_time = now
    
    for event in events:
      start_of_event = event.start
      if start_of_free_time < start_of_event:
        duration = (start_of_event - start_of_free_time).total_seconds() / 60
        if duration >= min_duration:
          free_times.append(FreeTime(id=make_uuid(), start = start_of_free_time, end = start_of_event))
      end_of_event = event.end
      start_of_free_time = max(start_of_free_time, end_of_event)

    # 最後のイベント後の空き時間も追加
    duration = (end - start_of_free_time).total_seconds() / 60
    if duration >= min_duration:
      free_times.append(FreeTime(id=make_uuid(), start=start_of_free_time, end=end))

    return free_times
  
  async def sync(self):
    calendar_repo = CalendarRepo(session=self.session)
    free_time_repo = FreeTimeRepo(session=self.session)
    events = await calendar_repo.get()
    free_times = await self._find_free_time(events)
    await free_time_repo.save(free_times)
  
  async def get(self): #TODO# need_syncの制御
    need_sync = True
    if need_sync:
      await self.sync()
    calendar_repo = CalendarRepo(session=self.session)
    free_time_repo = FreeTimeRepo(session=self.session)
    events = await calendar_repo.get()
    free_times = await free_time_repo.fetch_today()
    schedule = Schedule(id=make_uuid(), events=events, free_times=free_times)
    return schedule