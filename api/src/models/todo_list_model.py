from sqlalchemy import create_engine, Column, String
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
class TodoListModel(Base):
    __tablename__ = 'todo_list'

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    updated = Column(String)
    
    def __init__(self, todo_list_entity):
        self.id       = todo_list_entity.id
        self.title    = todo_list_entity.title
        self.updated  = todo_list_entity.updated

    def __repr__(self):
        return f"<TodoList(id={self.id}, title='{self.title}')>"

# テーブルの作成
Base.metadata.create_all(engine)

# セッションのクローズ
session.close()