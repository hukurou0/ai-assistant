from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

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
class TodoModel(Base):
    __tablename__ = 'todo'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    notes = Column(String)
    updated = Column(String)
    position = Column(String)
    status = Column(String)
    due = Column(String)
    difficulty = Column(Integer)
    required_time = Column(Integer)
    priority = Column(Integer)
    
    def __init__(self, todo_entity):
        self.id       = todo_entity.id
        self.title    = todo_entity.title
        self.notes    = todo_entity.notes
        self.updated  = todo_entity.updated
        self.position = todo_entity.position
        self.status   = todo_entity.status
        self.due      = todo_entity.due
        self.difficulty = 8
        self.required_time = 7
        self.priority = 6

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}')>"

# テーブルの作成
Base.metadata.create_all(engine)

# セッションのクローズ
session.close()