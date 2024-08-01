from domain.todo import Todo

tools = [
    {
        "type": "function",
        "function": {
            "name": "display_info",
            "description": "Displays detailed information about a specific task including its required time, priority level, and importance level.",
            "parameters": {
                "type": "object",
                "properties": {
                    "required_time": {
                        "type": "integer",
                        "description": Todo.Explanation.required_time,
                    },
                    "priority_level": {
                        "type": "integer",
                        "description": Todo.Explanation.priority_level,
                    },
                    "importance_level": {
                        "type": "integer",
                        "description": Todo.Explanation.importance_level,
                    },
                },
                "required": ["required_time", "priority_level", "importance_level"],
            },
        },
    }
]
