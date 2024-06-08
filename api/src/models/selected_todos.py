from src.models.make_base import Base
from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# テーブルの定義
class SelectedTodosModel(Base):
    __tablename__ = 'selected_todos'

    id    = Column(String, primary_key=True)
    date  = Column(DateTime(timezone=True))
    start = Column(DateTime(timezone=True))
    end   = Column(DateTime(timezone=True))
    todo_id = Column(String, ForeignKey('todo.id'))
    todo  = relationship("TodoModel", back_populates="selected_todos", lazy='select')
    
    def __init__(self, id, date, start, end, todo):
      self.id    = id
      self.date  = date
      self.start = start
      self.end   = end
      self.todo  = todo

    def __repr__(self):
      return f"id:{self.id}, date:{self.date}, start:{self.start}, end:{self.end}, todo:{self.todo}"