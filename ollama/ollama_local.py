from langchain_experimental.llms.ollama_functions import OllamaFunctions
from tools import tools

model = OllamaFunctions(model="llama3", format="json")
model = model.bind_tools(
    tools=[tools[0]["function"]],
    function_call={"name": "display_info"},
)
