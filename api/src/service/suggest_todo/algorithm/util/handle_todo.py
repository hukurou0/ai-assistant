from src.domain.entities.todo import Todo
from src.domain.vos.converted_todo_vo import ConvertedTodoVO


def convert_todos(todos: list[Todo], culc_value) -> list[ConvertedTodoVO]:
    converted_todos: list[ConvertedTodoVO] = []
    for todo in todos:
        if todo.required_time and todo.priority:
            value = culc_value(todo)
            converted_todos.append(
                ConvertedTodoVO(id=todo.id, value=value, time=todo.required_time)
            )
    return converted_todos


def revert_todo(converted_todo: ConvertedTodoVO, todos: list[Todo]) -> Todo:
    for todo in todos:
        if todo.id == converted_todo.id:
            return todo
