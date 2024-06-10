from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from fastapi import FastAPI, Depends, HTTPException
import yaml
from src.service.shared.component.calendar.google_calendar import GoogleCalendarComponent
from src.service.shared.component.todo.google_todo import GoogleTodoComponent
from src.service.suggest_todo import SuggestTodoService
from src.service.shared.component.evaluation.gpt4o.gpt4o_evaluation import GPT4OEvaluationComponent
from src.service.sync_todo import SyncTodoService
from src.service.shared.provider.local_todo import LocalTodoProvider
from src.service.selected_todo import SelectedTodosService 
from src.service.schedule import ScheduleService

from src.const import request_params 

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

# OpenAPIの仕様をファイルから読み込む
with open("./doc/v1.0.0.yaml", "r") as file:
    openapi_schema = yaml.safe_load(file)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

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

@app.get("/suggest")
async def suggest(free_time_id:str = None, db: AsyncSession = Depends(get_db_session)):
    calendar_component = GoogleCalendarComponent()
    todo_provider = LocalTodoProvider(session = db)  
    suggest_todo_service = SuggestTodoService(calendar_component=calendar_component, todo_provider=todo_provider)
    suggest_todos = await suggest_todo_service.find_well_todos()
    
    selected_todos = await SelectedTodosService(session = db).get_selected_todos_by_free_time_id(free_time_id)
    
    response_suggest_todos = []
    for suggest_todo in suggest_todos:
        response_suggest_todos.append(
            {
                "id"           : suggest_todo.todo.id,
                "title"        : suggest_todo.todo.title,
                "required_time": suggest_todo.todo.required_time,
                "notes"        : suggest_todo.todo.notes
            }
        )
        
    response_selected_todos = []
    for selected_todo in selected_todos:
        response_selected_todos.append(
            {
                "id"           : selected_todo.id,
                "title"        : selected_todo.title,
                "required_time": selected_todo.required_time,
                "notes"        : selected_todo.notes
            }
        )
        
    response = {
        "free_time_id":free_time_id,
        "suggest_todos":response_suggest_todos,
        "selected_todos":response_selected_todos
    }
        
    return response
    
@app.patch("/selected-todo/add")
async def add_selected_todo(request_body:request_params.SelectedTodoAddParams, db: AsyncSession = Depends(get_db_session)):
    message = await SelectedTodosService(session = db).add_selected_todo_by_id(request_body.todo_id,request_body.free_time_id)
    if message == "success":
        return {"todo_id": request_body.todo_id, "message": "success"}

@app.patch("/selected-todo/remove")
async def remove_selected_todo(request_body:request_params.SelectedTodoRemoveParams, db: AsyncSession = Depends(get_db_session)):
    message = await SelectedTodosService(session = db).delete_selected_todo_by_id(request_body.todo_id,request_body.free_time_id)
    if message == "success":
        return {"todo_id": request_body.todo_id, "message": "success"}

@app.get("/schedule")
async def get_schedule(db: AsyncSession = Depends(get_db_session)):
    schedule = await ScheduleService(session = db).get()
    sorted_elements = schedule.get_elements_sorted_by_time()
    response_schedule = []
    for sorted_element in sorted_elements:
        if sorted_element.__class__.__name__ == "Event":
            response_schedule.append({
                "type":"event",
                "id"         :sorted_element.id,
                "summary"    :sorted_element.summary,
                "description":sorted_element.description,
                "start"      :sorted_element.start,
                "end"        :sorted_element.end,
            })
        elif sorted_element.__class__.__name__ == "FreeTime":
            response_schedule.append({
                "type":"free_time",
                "id"   :sorted_element.id,
                "start":sorted_element.start,
                "end"  :sorted_element.end,
            })
    return {"schedule": response_schedule}