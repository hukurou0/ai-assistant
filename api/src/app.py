from src.app_setting import app, get_db_session, get_current_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from mangum import Mangum

from src.service.suggest_todo.suggest_todo import SuggestTodoService
from src.service.sync_todo import SyncTodoService
from src.service.shared.provider.local_todo import LocalTodoProvider
from src.service.selected_todo import SelectedTodosService
from src.service.schedule import ScheduleService
from src.service.user import UserService

from src.const import request_params


# ルートエンドポイント
@app.get("/")
async def read_root():
    return {"message": "hello world"}


# TODO# Google-todoで削除したときにsyncできるように（現状DBに残り続ける）
# TODO# Google-todoでtodoのみアップデートされた時syncできるように（listのupdatedが変わらないためスキップされる）
@app.get("/sync/google-todo")
async def sync_google(
    db: AsyncSession = Depends(get_db_session),
    user_id: str = Depends(get_current_user_id),
):
    # import time
    # start_time = time.time()

    sync_todo_service = SyncTodoService(session=db)
    result = await sync_todo_service.execute(user_id)

    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"所要時間: {elapsed_time}秒")

    if result == "finished":
        return {"message": "finished"}


@app.get("/suggest")
async def suggest(
    free_time_id: str = "",
    db: AsyncSession = Depends(get_db_session),
    user_id: str = Depends(get_current_user_id),
):
    todo_provider = LocalTodoProvider(session=db)
    suggest_todo_service = SuggestTodoService(session=db, todo_provider=todo_provider)
    suggest_todos = await suggest_todo_service.find_well_todos(user_id, free_time_id)

    selected_todos = await SelectedTodosService(
        session=db
    ).get_selected_todos_by_free_time_id(free_time_id)

    response_suggest_todos = []
    for suggest_todo in suggest_todos:
        response_suggest_todos.append(
            {
                "id": suggest_todo.todo.id,
                "title": suggest_todo.todo.title,
                "required_time": suggest_todo.todo.required_time,
                "notes": suggest_todo.todo.notes,
            }
        )

    response_selected_todos = []
    if selected_todos:
        for selected_todo in selected_todos:
            response_selected_todos.append(
                {
                    "id": selected_todo.id,
                    "title": selected_todo.title,
                    "required_time": selected_todo.required_time,
                    "notes": selected_todo.notes,
                }
            )

    response = {
        "free_time_id": free_time_id,
        "suggest_todos": response_suggest_todos,
        "selected_todos": response_selected_todos,
    }

    return response


@app.patch("/selected-todo/add")
async def add_selected_todo(
    request_body: request_params.SelectedTodoAddParams,
    db: AsyncSession = Depends(get_db_session),
    user_id: str = Depends(get_current_user_id),
):
    message = await SelectedTodosService(session=db).add_selected_todo_by_id(
        request_body.todo_id, request_body.free_time_id
    )
    if message == "success":
        return {"todo_id": request_body.todo_id, "message": "success"}


@app.patch("/selected-todo/remove")
async def remove_selected_todo(
    request_body: request_params.SelectedTodoRemoveParams,
    db: AsyncSession = Depends(get_db_session),
    user_id: str = Depends(get_current_user_id),
):
    message = await SelectedTodosService(session=db).delete_selected_todo_by_id(
        request_body.todo_id, request_body.free_time_id
    )
    if message == "success":
        return {"todo_id": request_body.todo_id, "message": "success"}


@app.get("/schedule")
async def get_schedule(
    db: AsyncSession = Depends(get_db_session),
):
    return {"message": "hello_world"}


@app.post("/signup")
async def signup(
    request_body: request_params.SigninParams,
    db: AsyncSession = Depends(get_db_session),
):
    user_service = UserService(session=db)
    tokens = await user_service.signup(
        access_token=request_body.access_token, refresh_token=request_body.refresh_token
    )
    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
    }


@app.get("/check")
async def check(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db_session),
):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTA3ODA0MDg1Njk5NjI4ODg4NTg5In0.Vu9PjOAGDmF5XjWZwg4l5UpdTcUYjzoEkHtSj1qq_PE"
    user = await UserService(session=db).get_user_by_id(user_id)


handler = Mangum(app)
