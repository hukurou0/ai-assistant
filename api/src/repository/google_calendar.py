from datetime import datetime, timedelta
import pytz

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.repository.shared.google_base import GoogleBase

from pydantic import BaseModel

from src.domain.entities.user import User

class GoogleCalendarRepo(GoogleBase, BaseModel):
  def _parse_event_datetime(self, event_start)->datetime:
    dt_str = event_start.get('dateTime') or event_start.get('date')
    dt = datetime.fromisoformat(dt_str)
    # タイムゾーン情報がない場合、日本のタイムゾーンを設定
    if dt.tzinfo is None:
        tz_japan = pytz.timezone('Asia/Tokyo')
        dt = tz_japan.localize(dt)
    return dt
  
  #TODO# 複数のカレンダーをon,off出来るように
  def get_events(self, user:User):
    creds = self.get_cred(user)
    try:
      service = build("calendar", "v3", credentials=creds)

      # Call the Calendar API
      tz_tokyo = pytz.timezone('Asia/Tokyo')
      now = datetime.now(tz_tokyo)
      end = now.replace(hour=20, minute=0, second=0, microsecond=0)
      # 現在時刻が20:00を過ぎている場合は、次の日の20:00を設定
      if now > end:
        end += timedelta(days=1)
      events_result = (
          service.events()
          .list(
              calendarId="primary",
              timeMin=now.isoformat(),
              timeMax=end.isoformat(),
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )
      events = events_result.get("items", [])
      
      class_result = (
          service.events()
          .list(
              calendarId="95409190d7447bc8f5c7be0d2f3a647c7f5c653098e46de726ee4ddff5a7d681@group.calendar.google.com",
              timeMin=now.isoformat(),
              timeMax=end.isoformat(),
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )
      class_times = class_result.get("items", [])
    except HttpError as error:
      print(f"An error occurred: {error}")
    
    all_events = events + class_times
    sorted_events = sorted(all_events, key=lambda x: self._parse_event_datetime(event_start = x['start']))  
    return sorted_events