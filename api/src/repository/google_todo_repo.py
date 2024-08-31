from sqlalchemy.future import select
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

from src.repository.shared.google_base import GoogleBase

from pydantic import BaseModel
from src.domain.entities.todo import Todo, TodoStatus
from src.domain.entities.user import User
from src.domain.entities.tag import Tag
from src.util.make_uuid import make_uuid
from src.models.tag_model import TagModel
from src.repository.tag_repo import TagMapper
from typing import Any


class GoogleTodoRepository(GoogleBase, BaseModel):
    session: Any

    async def _fetch_todo_list_id_title_map(self, creds) -> dict[str, str]:
        try:
            service = build("tasks", "v1", credentials=creds)

            # Call the Tasks API
            results = service.tasklists().list(maxResults=10).execute()
            items = results.get("items", [])
            id_title_map = {item["id"]: item["title"] for item in items}
            return id_title_map
        except HttpError as err:
            print(err)
            return err

    def map_google_task_status(self, google_task_status: str) -> TodoStatus:
        if google_task_status == "needsAction":
            return TodoStatus.TODO
        elif google_task_status == "completed":
            return TodoStatus.COMPLETED
        else:
            raise ValueError(f"Unknown Google Task status: {google_task_status}")

    def map_google_task_due(self, google_task_due: str) -> datetime:
        if google_task_due == "":
            return None
        return datetime.datetime.strptime(google_task_due, "%Y-%m-%dT%H:%M:%S.%fZ")

    async def _fetch_todos(
        self, creds, user: User, list_id: str, tag: Tag
    ) -> list[Todo]:
        try:
            service = build("tasks", "v1", credentials=creds)

            # Call the Tasks API
            results = service.tasks().list(tasklist=list_id).execute()
            items = results.get("items", [])
            todos = [
                Todo(
                    id=item["id"],
                    user=user,
                    title=item["title"],
                    notes=item.get("notes", ""),
                    status=self.map_google_task_status(item["status"]),
                    due=self.map_google_task_due(item.get("due", "")),
                    tags=[tag],
                )
                for item in items
            ]
            active_todos = [todo for todo in todos if todo.status == TodoStatus.TODO]

        except HttpError as err:
            print(err)

        return active_todos

    async def _tag_create(self, tag_entity: Tag):
        todo_model = TagMapper.to_model(tag_entity)
        self.session.add(todo_model)
        await self.session.commit()

    async def _tag_find(self, tag_name, user: User):
        result = await self.session.execute(
            select(TagModel).filter(
                TagModel.name == tag_name, TagModel.user_id == user.id
            )
        )
        tag_model = result.scalars().first()
        tag = TagMapper.to_entity(tag_model, user) if tag_model else None
        return tag

    async def fetch_todos(self, user: User) -> list[Todo]:
        creds = self.get_cred(user)
        id_title_map = await self._fetch_todo_list_id_title_map(creds)
        all_todos = []
        for list_id in list(id_title_map.keys()):
            tag = await self._tag_find(id_title_map[list_id], user)
            if not tag:
                tag = Tag(id=make_uuid(), name=id_title_map[list_id], user=user)
                await self._tag_create(tag)
            todos = await self._fetch_todos(creds, user, list_id, tag)
            all_todos.extend(todos)
        return all_todos
