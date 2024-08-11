from datetime import datetime, timedelta, date
import pytz


def get_now_datetime():
    return datetime.now(pytz.timezone("Asia/Tokyo"))


def get_today_date():
    now = get_now_datetime()
    if now.hour < 20:
        today_date = now.replace(hour=0, minute=0, second=0, microsecond=0).date()
    else:
        today_date = (
            (now + timedelta(days=1))
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .date()
        )
    return today_date


def get_start_of_datetime(target_date: date) -> datetime:
    tokyo_tz = pytz.timezone("Asia/Tokyo")
    start_of_day = tokyo_tz.localize(datetime.combine(target_date, datetime.min.time()))
    return start_of_day


def get_start_end_time(
    target_date: date, start_time: int, end_time: int
) -> tuple[datetime, datetime]:
    start_of_day = get_start_of_datetime(target_date)
    start = start_of_day.replace(hour=start_time, minute=0, second=0, microsecond=0)
    end = start_of_day.replace(hour=end_time, minute=0, second=0, microsecond=0)
    if start > end:
        end += timedelta(days=1)
    return start, end
