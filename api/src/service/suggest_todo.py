from src.service.shared.provider.local_todo import LocalTodoProvider

from typing import Union
from pydantic import BaseModel
from typing import Any
from src.domain.vos.suggest_todo import SuggestTodoVO
from src.domain.vos.free_time import FreeTimeVO

from src.repository.google_calendar import GoogleCalendarRepo
from src.repository.user_repo import UserRepo

from datetime import datetime, timedelta
import pytz

class SuggestTodoService(BaseModel):
  session:Any
  todo_provider:Union[LocalTodoProvider]

  #TODO# min_durationを設定できるように
  def _find_free_times(self, events, min_duration:int=15)->list[FreeTimeVO]: 
         
    free_times:list[FreeTimeVO] = []
    tz_tokyo = pytz.timezone('Asia/Tokyo')
    now = datetime.now(tz_tokyo)
    #TODO# 終了時間調整できるように
    end = now.replace(hour=20, minute=0, second=0, microsecond=0)
    # 現在時刻が20:00を過ぎている場合は、次の日の20:00を設定
    if now > end:
      end += timedelta(days=1)
    #end = now + timedelta(days=1)
    start_of_free_time = now
    
    for event in events:
      start_of_event = tz_tokyo.localize(datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))).replace(tzinfo=None))
      if start_of_free_time < start_of_event:
        duration = (start_of_event - start_of_free_time).total_seconds() / 60
        if duration >= min_duration:
          free_times.append(FreeTimeVO(duration = int(duration), start = start_of_free_time, end = start_of_event))
      end_of_event = tz_tokyo.localize(datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date'))).replace(tzinfo=None))
      start_of_free_time = max(start_of_free_time, end_of_event)

    # 最後のイベント後の空き時間も追加
    if start_of_free_time < end:
      duration = int((end - start_of_free_time).total_seconds() / 60)
      free_times.append(FreeTimeVO(duration = duration, start = start_of_free_time, end = end))

    return free_times

  async def find_well_todos(self, user) -> list[SuggestTodoVO]: 
    user_repo = UserRepo(session = self.session)
    user = await user_repo.fetch_user_by_id(user.id)
    
    google_calendar_repo = GoogleCalendarRepo(session = self.session)
    events = google_calendar_repo.get_events(user)
    free_times = self._find_free_times(events)
    todos = await self.todo_provider.fetch_todos()

    well_todos:list[SuggestTodoVO] = []
    for free_time in free_times:
      duration = free_time.duration
      for i, todo in enumerate(todos):
        if todo.required_time:
          if duration >= todo.required_time:
            well_todo = SuggestTodoVO(
                            free_time=free_time,
                            todo=todo
                        )
            well_todos.append(well_todo)
            duration -= todo.required_time
            del todos[i]
            
    return well_todos
    
