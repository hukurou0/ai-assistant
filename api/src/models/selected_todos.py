from src.models.make_base import Base
from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.models.todo_list_model import TodoModel

# テーブルの定義
class SelectedTodosModel(Base):
    __tablename__ = 'selected_todos'

    id           = Column(String, primary_key=True)
    date         = Column(DateTime(timezone=True))
    free_time_id = Column(String, ForeignKey('free_time.id'))
    todo_id      = Column(String, ForeignKey('todo.id'))
    
    todo      = relationship("TodoModel", back_populates="selected_todos")
    free_time = relationship("FreeTimeModel", back_populates="selected_todos")
    
    def __init__(self, id, date, free_time_id, todo_id):
      self.id    = id
      self.date  = date
      self.free_time_id = free_time_id
      self.todo_id = todo_id

    def __repr__(self):
      return f"id:{self.id}, date:{self.date}, start:{self.start}, end:{self.end}, todo:{self.todo}"