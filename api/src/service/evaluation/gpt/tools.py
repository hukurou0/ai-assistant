tools = [
    {
        "type":"function",
        "function":{
            "name": "display_info",
            "description": "Show users how difficult a task is and how long it will taken",
            "parameters": {
                "type": "object",
                "properties": {
                    "difficulty": {
                        "type": "integer",
                        "description": "Score the difficulty of the task on a scale of 1-10",
                    },
                    "required_time": {
                        "type": "integer", 
                        "description": "Number of minutes it takes to perform the task."
                    },
                    "priority": {
                        "type": "integer",
                        "description": "Score the priority of the task on a scale of 1-10",
                    },
                },
                "required": ["difficulty", "required_time","priority"],
            },
        }
        
    }
]