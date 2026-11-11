
from dotenv import load_dotenv
from typing import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from IPython.display import Image, display
load_dotenv()

model=init_chat_model(
    "deepseek-v4-flash",
    extra_body={"thinking":{"type":"disabled"}}
)

class LLMState(TypedDict):
    input:str
    output:str



def llm_node(state:LLMState):
    response= model.invoke(state["input"])
    return {"output":response.text}


graph= StateGraph(LLMState)
graph.add_node("llm_node", llm_node)

graph.add_edge(START, "llm_node")

graph.add_edge("llm_node", END)
builder=graph.compile()
result=builder.invoke({"input":"hello"})
print(result)
display(Image(builder.get_graph(xray=True).draw_mermaid_png()))




