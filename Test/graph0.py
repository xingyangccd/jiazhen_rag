from typing import TypedDict

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from rich.jupyter import display

from IPython.display import Image, display


class DefaultReducerState(TypedDict):
    var: str

def Node_1(state:DefaultReducerState):
    print("node1接受收到了state")
    return {"var":"node_1 value"}

def Node_2(state:DefaultReducerState):
    print("node2接受收到了state")
    return {"var":"node_2 value"}

graph_builder = StateGraph(DefaultReducerState)
graph_builder.add_node("node_1", Node_1)
graph_builder.add_node("node_2", Node_2)
graph_builder.add_edge(START, "node_1")
graph_builder.add_edge("node_1", "node_2")
graph_builder.add_edge("node_2", END)

graph = graph_builder.compile()

result = graph.invoke({"name": "World"})
print(result)
display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
