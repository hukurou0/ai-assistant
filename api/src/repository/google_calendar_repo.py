from pydantic import BaseModel
from typing import Any
from src.domain.entities.event import Event
from src.domain.entities.user import User

from src.repository.shared.google_base import GoogleBase

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from datetime import datetime, timedelta
import pytz
from src.util.handle_time import get_today_date, get_start_of_datetime


class GoogleCalendarRepo(GoogleBase, BaseModel):
    session: Any

    def _parse_event(self, event) -> Event:
        return Event(
            id=event["id"],
            summary=event.get("summary", ""),
            description=event.get("description", ""),
            start=self._parse_event_datetime(event["start"]),
            end=self._parse_event_datetime(event["end"]),
        )

    def _parse_event_datetime(self, event_start) -> datetime:
        dt_str = event_start.get("dateTime") or event_start.get("date")
        dt = datetime.fromisoformat(dt_str)
        # タイムゾーン情報がない場合、日本のタイムゾーンを設定
        if dt.tzinfo is None:
            tz_japan = pytz.timezone("Asia/Tokyo")
            dt = tz_japan.localize(dt)
        return dt

    async def get(self, user: User) -> list[Event]:
        creds = self.get_cred(user)
        try:
            service = build("calendar", "v3", credentials=creds)

            # Call the Calendar API
            start_of_day = get_start_of_datetime(get_today_date())
            end_of_day = start_of_day.replace(
                hour=20, minute=0, second=0, microsecond=0
            )
            # 現在時刻が20:00を過ぎている場合は、次の日の20:00を設定
            if start_of_day > end_of_day:
                end_of_day += timedelta(days=1)

            calendar_list = service.calendarList().list().execute()
            events = []
            calendar_ids = [calendar["id"] for calendar in calendar_list["items"]]
            for calendar_id in calendar_ids:
                events_result = (
                    service.events()
                    .list(
                        calendarId=calendar_id,
                        timeMin=start_of_day.isoformat(),
                        timeMax=end_of_day.isoformat(),
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
                events.extend(events_result.get("items", []))
        except HttpError as error:
            print(f"An error occurred when fetch events from Google Calendar: {error}")

        sorted_events = sorted(
            events, key=lambda x: self._parse_event_datetime(event_start=x["start"])
        )
        return [self._parse_event(event) for event in sorted_events]
