from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException
from src.service.calendar.cloud.google_calendar import GoogleCalendarService
from src.service.todo.cloud.google_todo import GoogleTodoService
from src.service.suggest_todo import SuggestTodoService
from src.service.llm.gpt.evaluation import GPT4EvaluationService
from src.service.todo.cloud.sync_todo import SyncTodoService
from src.service.todo.local_todo import LocalTodoService

# データベース設定
DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@postgres/mydatabase"

# SQLAlchemy用のエンジンを作成
engine = create_async_engine(
  DATABASE_URL, 
  #echo=True,
  pool_size=5,          # プール内のコネクション数
  max_overflow=10,      # プールサイズを超えた際の最大数
  pool_timeout=30,      # プールからコネクションを取得する際のタイムアウト秒数
  pool_recycle=-1       # コネクションを再利用するための時間（秒）、デフォルトではリサイクルしない
)

# セッションを作成するためのファクトリーを生成
async_session = sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession,
    autocommit=False
)

# FastAPI アプリケーション
app = FastAPI()

# 依存関係
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# ルートエンドポイント
@app.get("/")
async def read_root():
    return {"message": "hello_world"}

#TODO# Google-todoで削除したときにsyncできるように（現状DBに残り続ける）
@app.get("/sync/google-todo")
async def sync_google(db: AsyncSession = Depends(get_db_session)):
    todo_service = GoogleTodoService(session = db)
    evaluation_service = GPT4EvaluationService(session = db)
    sync_todo_service = SyncTodoService(todo_service=todo_service, evaluation_service=evaluation_service)
    result = await sync_todo_service.execute()
    if result == "success":
        return {"message": "success"}
    
  
@app.get("/find")
async def read_root(db: AsyncSession = Depends(get_db_session)):
    calendar_service = GoogleCalendarService()
    todo_service = LocalTodoService(session = db)  
    suggest_todo_service = SuggestTodoService(calendar_service=calendar_service, todo_service=todo_service)
    well_todos = await suggest_todo_service.find_well_todos()
    
    response_well_todos = []
    for well_todo in well_todos:
        free_time = well_todo.free_time
        todo = well_todo.todo
        
        response_well_todo = {
            "free_time":{
                "start":free_time.start,
                "end":free_time.end,
                "duration":free_time.duration
            },
            "todo":{
                "title":todo.title,
                "required_time":todo.required_time,
                "difficulty":todo.difficulty
            }
        }
        response_well_todos.append(response_well_todo)
        
    return {"well_todos": response_well_todos}
