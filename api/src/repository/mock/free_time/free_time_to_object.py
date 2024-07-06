from src.domain.entities.free_time import FreeTime
import json
from datetime import datetime


def load_free_time_from_json(file_path: str) -> FreeTime:
    with open(file_path, "r", encoding="utf-8") as f:
        free_time_data = json.load(f)
        free_time_data["start"] = datetime.fromisoformat(free_time_data["start"])
        free_time_data["end"] = datetime.fromisoformat(free_time_data["end"])
        free_time = FreeTime(**free_time_data)
    return free_time


""" import json
with open('free_time.json', 'w', encoding='utf-8') as f:
  json.dump(free_time.dict(), f, ensure_ascii=False, indent=4, default=str) """
