from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from rich.jupyter import display

from IPython.display import Image, display


class SimpleState(TypedDict):
    name: str
    greeting: str  # 记录生成的问候语


def Node_1(state: SimpleState) -> SimpleState:
    name = state.get("name")
    greeting = f"hello{name}"
    print("node1_执行中接受name=" + name)
    return {"greeting": greeting}


def Node_2(state: SimpleState) -> SimpleState:
    greeting = state.get("greeting").upper()
    print("node2_执行中接受greeting=" + greeting)
    return {"greeting": greeting}


graph_builder = StateGraph(SimpleState)
graph_builder.add_node("node_1", Node_1)
graph_builder.add_node("node_2", Node_2)
graph_builder.add_edge(START, "node_1")
graph_builder.add_edge("node_1", "node_2")
graph_builder.add_edge("node_2", END)

graph = graph_builder.compile()

result = graph.invoke({"name": "World"})
print(result)
display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
