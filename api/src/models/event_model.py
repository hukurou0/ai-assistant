from src.models.make_base import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


# テーブルの定義
class EventModel(Base):
    __tablename__ = "event"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("app_user.id"))
    summary = Column(String)
    description = Column(String)
    start = Column(DateTime(timezone=True))
    end = Column(DateTime(timezone=True))

    def __init__(self, id, user_id, summary, description, start, end):
        self.id = id
        self.user_id = user_id
        self.summary = summary
        self.description = description
        self.start = start
        self.end = end

    def __repr__(self):
        return f"EventModel(id:{self.id}, user_id:{self.user_id}, summary:{self.summary}, description:{self.description}, start:{self.start}, end:{self.end})"
