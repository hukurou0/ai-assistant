from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import selectinload

from src.domain.entities.event import Event

from pydantic import BaseModel
from typing import Any

from src.repository.shared.google_base import GoogleBase

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import datetime, timedelta
import pytz

class CalendarRepo(GoogleBase,BaseModel):
  session:Any
  
  def _parse_event(self, event) -> Event:
    return Event(
      id = event["id"],
      summary = event.get("summary", ""),
      description = event.get("description", ""),
      start = self._parse_event_datetime(event["start"]),
      end = self._parse_event_datetime(event["end"]),
    )
    
  def _parse_event_datetime(self, event_start)->datetime:
    dt_str = event_start.get('dateTime') or event_start.get('date')
    dt = datetime.fromisoformat(dt_str)
    # タイムゾーン情報がない場合、日本のタイムゾーンを設定
    if dt.tzinfo is None:
        tz_japan = pytz.timezone('Asia/Tokyo')
        dt = tz_japan.localize(dt)
    return dt
  
  async def get(self) -> list[Event]:
    creds = self.get_cred()
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
    return [self._parse_event(event) for event in sorted_events]