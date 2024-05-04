from datetime import datetime, timedelta
import os.path
import pytz

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.cloud.common.google_base import GoogleBase

from src.domain.vos.free_time import FreeTimeVO

class GoogleCalendar(GoogleBase):
  def __init__(self):
    self.events = []
  
  #TODO# min_durationを設定できるように
  def find_free_times(self, min_duration:int=15)->list[FreeTimeVO]:
    """ for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"]) """
      
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
    
    for event in self.events:
      start_of_event = tz_tokyo.localize(datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))).replace(tzinfo=None))
      if start_of_free_time < start_of_event:
        duration = (start_of_event - start_of_free_time).total_seconds() / 60
        if duration >= min_duration:
          free_times.append(FreeTimeVO(duration = duration, start = start_of_free_time, end = start_of_event))
      end_of_event = tz_tokyo.localize(datetime.fromisoformat(event['end'].get('dateTime', event['end'].get('date'))).replace(tzinfo=None))
      start_of_free_time = max(start_of_free_time, end_of_event)

    # 最後のイベント後の空き時間も追加
    if start_of_free_time < end:
      duration = (end - start_of_free_time).total_seconds() / 60
      free_times.append(FreeTimeVO(duration = duration, start = start_of_free_time, end = end))
        
    return free_times
  
  #TODO# 複数のカレンダーをon,off出来るように
  def get_events(self):
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
    sorted_events = sorted(all_events, key=lambda x: datetime.fromisoformat(x['start'].get('dateTime', x['start'].get('date'))))  
    self.events = sorted_events