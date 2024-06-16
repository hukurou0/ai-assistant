from src.models.make_base import Base
from sqlalchemy import Column, String

# テーブルの定義
class UserModel(Base):
    __tablename__ = 'app_user'

    id    = Column(String, primary_key=True)
    email = Column(String)
    name  = Column(String)
    picture_url   = Column(String)
    access_token  = Column(String)
    refresh_token = Column(String)
    
    def __init__(self, id, email, name, picture_url, access_token, refresh_token):
      self.id    = id
      self.email = email
      self.name  = name
      self.picture_url   = picture_url
      self.access_token  = access_token
      self.refresh_token = refresh_token