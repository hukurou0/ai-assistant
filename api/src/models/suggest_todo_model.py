from src.models.make_base import Base
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


# テーブルの定義
class SuggestTodoModel(Base):
    __tablename__ = "suggest_todo"

    id = Column(String, primary_key=True)
    todo_id = Column(String, ForeignKey("todo.id"))
    free_time_id = Column(String, ForeignKey("free_time.id"))
    selected = Column(Boolean)

    todo = relationship("TodoModel", back_populates="suggest_todo")
    free_time = relationship("FreeTimeModel", back_populates="suggest_todo")

    def __init__(self, id, todo_id, free_time_id, selected):
        self.id = id
        self.todo_id = todo_id
        self.free_time_id = free_time_id
        self.selected = selected

    def __repr__(self):
        return f"<SuggestTodoModel(id={self.id}, todo_id={self.todo_id}, free_time_id={self.free_time_id}, selected={self.selected})>"
