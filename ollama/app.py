from fastapi import FastAPI
from ollama_local import model
from pydantic import BaseModel

app = FastAPI()


class LocalEvaluateParams(BaseModel):
    todo_id: str
    content: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/local_evaluate")
def evaluate(request_body: LocalEvaluateParams):
    model_response = model.invoke(request_body.content)
    if model_response.tool_calls:
        evaluation_params = model_response.tool_calls[0]["args"]
        response = {
            "todo_id": request_body.todo_id,
            "required_time": evaluation_params["required_time"],
            "priority_level": evaluation_params["priority_level"],
            "importance_level": evaluation_params["importance_level"],
        }
    return response
