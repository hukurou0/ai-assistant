from fastapi import FastAPI
from ollama_local import model

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/local")
def local():
    response = model.invoke("what is the weather in Boston?")
    print(response)
    return {"Hello": response}
