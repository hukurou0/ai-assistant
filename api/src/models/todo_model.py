from src.models.make_base import Base
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, ARRAY
from sqlalchemy.orm import relationship

from src.domain.entities.todo import Todo


# テーブルの定義
class TodoModel(Base):
    __tablename__ = "todo"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("app_user.id"))
    title = Column(String, nullable=False)
    notes = Column(String)
    status = Column(String)
    due = Column(DateTime(timezone=True))
    tag_ids = Column(ARRAY(String))
    required_time = Column(Integer)
    priority_level = Column(Integer)
    importance_level = Column(Integer)

    suggest_todo = relationship(
        "SuggestTodoModel", back_populates="todo", lazy="select"
    )

    def __init__(self, todo_entity: Todo):
        self.id = todo_entity.id
        self.user_id = todo_entity.user.id
        self.title = todo_entity.title
        self.notes = todo_entity.notes
        self.status = todo_entity.status
        self.due = todo_entity.due
        self.tag_ids = [tag.id for tag in todo_entity.tags]
        self.required_time = (
            todo_entity.required_time if hasattr(todo_entity, "required_time") else None
        )
        self.priority_level = (
            todo_entity.priority_level
            if hasattr(todo_entity, "priority_level")
            else None
        )
        self.importance_level = (
            todo_entity.importance_level
            if hasattr(todo_entity, "importance_level")
            else None
        )

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}')>"
