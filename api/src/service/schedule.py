from pydantic import BaseModel
from typing import Any
from src.repository.calendar_repo import CalendarRepo
from src.repository.free_time_repo import FreeTimeRepo

from src.domain.entities.schedule import Schedule
from src.domain.entities.free_time import FreeTime

from src.service.shared.utils.make_uuid import make_uuid

class ScheduleService(BaseModel):
  session:Any
  
  def _find_free_time(events) -> list[FreeTime]:
    pass
  
  async def sync(self):
    calendar_repo = CalendarRepo(session=self.session)
    free_time_repo = FreeTimeRepo(session=self.session)
    events = await calendar_repo.get()
    free_times = self._find_free_time(events)
    await free_time_repo.save(free_times)
  
  async def get(self):
    self.sync()
    calendar_repo = CalendarRepo(session=self.session)
    free_time_repo = FreeTimeRepo(session=self.session)
    events = await calendar_repo.get()
    free_times = await free_time_repo.fetch()
    schedule = Schedule(id=make_uuid(), events=events, free_times=free_times)
    return schedule