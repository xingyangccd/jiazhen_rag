
from dotenv import load_dotenv
from typing import TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from IPython.display import Image, display
load_dotenv()

model=init_chat_model(
    "deepseek-v4-flash",
    extra_body={"thinking":{"type":"disabled"}}
)

class LLMState(TypedDict):
    input:HumanMessage
    output:AIMessage



def llm_node(state:LLMState):
    response= model.invoke([state["input"]])
    return {"output":response}


graph= StateGraph(LLMState)
graph.add_node("llm_node", llm_node)

graph.add_edge(START, "llm_node")

graph.add_edge("llm_node", END)
builder=graph.compile()
result=builder.invoke({"input":HumanMessage(content="hello")})
print(result)
display(Image(builder.get_graph(xray=True).draw_mermaid_png()))