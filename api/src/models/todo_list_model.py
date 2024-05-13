from sqlalchemy import create_engine, Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from src.domain.entities.todo import Todo
from src.domain.entities.todo_list import TodoList

# データベースの接続情報
database_url = 'postgresql://myuser:mypassword@postgres/mydatabase'

# エンジンの作成
engine = create_engine(database_url)

# セッションの作成
Session = sessionmaker(bind=engine)
session = Session()

# Baseクラスの作成
Base = declarative_base()

# テーブルの定義
class TodoListModel(Base):
    __tablename__ = 'todo_list'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    updated = Column(DateTime(timezone=True))
    last_evaluation = Column(DateTime(timezone=True))
    todos = relationship("TodoModel", back_populates="todo_list", lazy='select')
    
    def __init__(self, todo_list_entity:TodoList):
        self.id       = todo_list_entity.id
        self.title    = todo_list_entity.title
        self.updated  = todo_list_entity.updated
        self.last_evaluation  = todo_list_entity.last_evaluation

    def __repr__(self):
        return f"<TodoList(id={self.id}, title='{self.title}', updated='{self.updated}', last_evaluation='{self.last_evaluation}')>"

class TodoModel(Base):
    __tablename__ = 'todo'

    id = Column(String, primary_key=True)
    todo_list_id = Column(String, ForeignKey('todo_list.id'))
    title = Column(String, nullable=False)
    notes = Column(String)
    updated = Column(String)
    position = Column(String)
    status = Column(String)
    due = Column(String)
    difficulty = Column(Integer)
    required_time = Column(Integer)
    priority = Column(Integer)
    todo_list = relationship("TodoListModel", back_populates="todos")
    
    def __init__(self, todo_entity:Todo, todo_list_model:TodoListModel):
        self.id           = todo_entity.id
        self.todo_list_id = todo_list_model.id
        self.title        = todo_entity.title
        self.notes        = todo_entity.notes
        self.updated      = todo_entity.updated
        self.position     = todo_entity.position
        self.status       = todo_entity.status
        self.due          = todo_entity.due
        self.difficulty    = todo_entity.difficulty if hasattr(todo_entity, 'difficulty') else None
        self.required_time = todo_entity.required_time if hasattr(todo_entity, 'required_time') else None
        self.priority      = todo_entity.priority if hasattr(todo_entity, 'priority') else None
        self.todo_list     = todo_list_model

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}')>"

# テーブルの作成
Base.metadata.create_all(engine)

# セッションのクローズ
session.close()