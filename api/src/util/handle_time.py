from datetime import datetime, timedelta
import pytz


def get_today_date():
    now = datetime.now(pytz.timezone("Asia/Tokyo"))
    if now.hour < 20:
        today_date = now.replace(hour=0, minute=0, second=0, microsecond=0).date()
    else:
        today_date = (
            (now + timedelta(days=1))
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .date()
        )
    return today_date
