from src.models.make_base import Base
from sqlalchemy import Column, String, ForeignKey


# テーブルの定義
class TagModel(Base):
    __tablename__ = "tag"

    id = Column(String, primary_key=True)
    name = Column(String)
    user_id = Column(String, ForeignKey("app_user.id"))

    def __init__(self, id, name, user_id):
        self.id = id
        self.name = name
        self.user_id = user_id
