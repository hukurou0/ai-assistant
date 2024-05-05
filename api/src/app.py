from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException
from src.service.calendar.cloud.google_calendar import GoogleCalendarService
from src.service.todo.cloud.google_todo import GoogleTodoService
from src.service.suggest_todo import SuggestTodoService

# データベース設定
DATABASE_URL = "postgresql+asyncpg://myuser:mypassword@postgres/mydatabase"

# SQLAlchemy用のエンジンを作成
engine = create_async_engine(
  DATABASE_URL, 
  echo=True,
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
async def read_root(db: AsyncSession = Depends(get_db_session)):
    async with db.begin():
        result = await db.execute(text("SELECT 'Hello, World!'"))
        hello_world = result.scalar_one()
        print(hello_world)
    return {"message": hello_world}
  
@app.get("/find")
async def read_root(db: AsyncSession = Depends(get_db_session)):
    calendar_service = GoogleCalendarService()
    todo_service = GoogleTodoService(session = db)
    suggest_todo_service = SuggestTodoService(calendar_service=calendar_service, todo_service=todo_service)
    well_todos = await suggest_todo_service.find_well_todos()
    
    response_well_todos = []
    for well_todo in well_todos:
        print(well_todo)
        free_time = well_todo.free_time
        todo = well_todo.complete_todo
        print(free_time)
        
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
