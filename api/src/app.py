from src.app_setting import app, get_db_session, get_current_user_id
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.service.suggest_todo.suggest_todo_service import SuggestTodoService
from src.service.sync_todo import SyncTodoService
from src.service.selected_todo import SelectedTodosService
from src.service.schedule import ScheduleService
from src.service.user import UserService

from src.const import request_params

from src.util.handle_time import get_now_datetime


# ルートエンドポイント
@app.get("/")
async def read_root():
    return {"message": "hello_world"}


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
    suggest_todo_service = SuggestTodoService(session=db)
    free_time_id, suggest_todos = await suggest_todo_service.get_suggest_todos(
        user_id, free_time_id
    )

    response_suggest_todos = []
    for suggest_todo in suggest_todos:
        response_suggest_todos.append(
            {
                "suggest_todo": {
                    "id": suggest_todo.id,
                    "title": suggest_todo.title,
                    "required_time": suggest_todo.required_time,
                    "notes": suggest_todo.notes,
                },
                "selected": suggest_todo.selected,
            }
        )

    response = {
        "free_time_id": free_time_id,
        "suggest_todos": response_suggest_todos,
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
    need_sync: bool,
    db: AsyncSession = Depends(get_db_session),
    user_id: str = Depends(get_current_user_id),
):
    schedule = await ScheduleService(session=db).get_today(user_id, need_sync)
    sorted_elements = schedule.get_elements_sorted_by_time()
    response_schedule = []
    for sorted_element in sorted_elements:
        if sorted_element.__class__.__name__ == "Event":
            response_schedule.append(
                {
                    "type": "event",
                    "id": sorted_element.id,
                    "summary": sorted_element.summary,
                    "description": sorted_element.description,
                    "time": sorted_element.start.strftime("%H:%M")
                    + " - "
                    + sorted_element.end.strftime("%H:%M"),
                    "now": sorted_element.start
                    <= get_now_datetime()
                    <= sorted_element.end,
                }
            )
        elif sorted_element.__class__.__name__ == "FreeTime":
            response_schedule.append(
                {
                    "type": "free_time",
                    "id": sorted_element.id,
                    "time": sorted_element.start.strftime("%H:%M")
                    + " - "
                    + sorted_element.end.strftime("%H:%M"),
                    "now": sorted_element.start
                    <= get_now_datetime()
                    <= sorted_element.end,
                }
            )
    return {"schedule": response_schedule}


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
        "access_token_expires_in": tokens["access_token_expires_in"],
        "refresh_token_expires_in": tokens["refresh_token_expires_in"],
    }


@app.post("/refresh")
async def refresh(
    request_body: request_params.RefreshTokenParams,
    db: AsyncSession = Depends(get_db_session),
):
    new_access_token, access_token_expires_in = await UserService(
        session=db
    ).token_refresh(request_body.refresh_token)
    return {
        "access_token": new_access_token,
        "access_token_expires_in": access_token_expires_in,
    }
