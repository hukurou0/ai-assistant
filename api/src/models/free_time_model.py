from src.models.make_base import Base
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship


# テーブルの定義
class FreeTimeModel(Base):
    __tablename__ = "free_time"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("app_user.id"))
    start = Column(DateTime(timezone=True))
    end = Column(DateTime(timezone=True))

    suggest_todo = relationship(
        "SuggestTodoModel", back_populates="free_time", lazy="select"
    )

    def __init__(self, id, user_id, start, end):
        self.id = id
        self.user_id = user_id
        self.start = start
        self.end = end

    def __repr__(self):
        return f"id:{self.id}, start:{self.start}, end:{self.end}"
