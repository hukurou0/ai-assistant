from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException
from src.service.shared.component.calendar.google_calendar import GoogleCalendarComponent
from src.service.shared.component.todo.google_todo import GoogleTodoComponent
from src.service.suggest_todo import SuggestTodoService
from src.service.shared.component.evaluation.gpt4o.gpt4o_evaluation import GPT4OEvaluationComponent
from src.service.sync_todo import SyncTodoService
from src.service.shared.provider.local_todo import LocalTodoProvider
from src.service.selected_todo import SelectedTodosService 

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
#TODO# Google-todoでtodoのみアップデートされた時syncできるように（listのupdatedが変わらないためスキップされる）
@app.get("/sync/google-todo")
async def sync_google(db: AsyncSession = Depends(get_db_session)):
    #import time
    #start_time = time.time()
    
    todo_component = GoogleTodoComponent(session = db)
    evaluation_component = GPT4OEvaluationComponent(session = db)
    sync_todo_service = SyncTodoService(todo_component=todo_component, evaluation_component=evaluation_component)
    result = await sync_todo_service.execute()
    
    #end_time = time.time()
    #elapsed_time = end_time - start_time
    #print(f"所要時間: {elapsed_time}秒")
    
    if result == "finished":
        return {"message": "finished"}
    
  
@app.get("/find")
async def read_root(db: AsyncSession = Depends(get_db_session)):
    calendar_component = GoogleCalendarComponent()
    todo_provider = LocalTodoProvider(session = db)  
    suggest_todo_service = SuggestTodoService(calendar_component=calendar_component, todo_provider=todo_provider)
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

@app.patch("/selected-todo/add")
async def add_selected_todo(todo_id: str = None, db: AsyncSession = Depends(get_db_session)):
    from src.domain.vos.free_time import FreeTimeVO
    from datetime import datetime
    free_time = FreeTimeVO(start = datetime.now(), end = datetime.now(), duration = 10)
    await SelectedTodosService(session = db).add_selected_todo_by_id(todo_id,free_time)
    return {"todo_id": todo_id, "message": "success"}