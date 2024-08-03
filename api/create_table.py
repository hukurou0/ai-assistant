from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.make_base import Base

# from src.models.selected_todos import SelectedTodosModel
from src.models.todo_list_model import TodoListModel, TodoModel
from src.models.free_time_model import FreeTimeModel
from src.models.user_model import UserModel
from src.models.suggest_todo_model import SuggestTodoModel

# データベースの接続情報
database_url = "postgresql://myuser:mypassword@postgres/mydatabase"

# エンジンの作成
engine = create_engine(database_url)

# セッションの作成
Session = sessionmaker(bind=engine)
session = Session()

# テーブルの作成
Base.metadata.create_all(engine)

# セッションのクローズ
session.close()
