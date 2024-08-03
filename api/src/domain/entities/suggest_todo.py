from pydantic import BaseModel
from src.domain.entities.todo import Todo
from src.domain.vos.suggest_todo_vo import SuggestTodoVO
from src.domain.entities.free_time import FreeTime


class SuggestTodo(BaseModel):
    id: str
    todo: Todo
    selected: bool

    def to_vo(self) -> SuggestTodoVO:
        return SuggestTodoVO(
            id=self.id,
            title=self.todo.title,
            required_time=self.todo.required_time,
            notes=self.todo.notes,
            selected=self.selected,
        )


class SuggestTodos(BaseModel):
    free_time: FreeTime
    suggest_todos: list[SuggestTodo]

    def to_vos(self) -> list[SuggestTodoVO]:
        return [suggest_todo.to_vo() for suggest_todo in self.suggest_todos]
