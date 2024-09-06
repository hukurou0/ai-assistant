from src.models.make_base import Base
from sqlalchemy import Column, String, ForeignKey
from src.domain.entities.tag import Tag


# テーブルの定義
class TagModel(Base):
    __tablename__ = "tag"

    id = Column(String, primary_key=True)
    name = Column(String)
    user_id = Column(String, ForeignKey("app_user.id"))

    def __init__(self, tag_entity: Tag):
        self.id = tag_entity.id
        self.name = tag_entity.name
        self.user_id = tag_entity.user.id
