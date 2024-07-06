from src.domain.entities.todo import Todo
import json


def load_todos_from_json(file_path: str) -> list[Todo]:
    with open(file_path, "r", encoding="utf-8") as f:
        todos_data = json.load(f)
        todos = [Todo(**todo) for todo in todos_data]
    return todos


""" import json
with open('todos.json', 'w', encoding='utf-8') as f:
    json.dump([todo.dict() for todo in todos], f, ensure_ascii=False, indent=4) """
