from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from rich.jupyter import display

from IPython.display import Image, display


def add(old,new):
    return old+new

class CustomReducerState(TypedDict):
    count: int
    nodes: Annotated[list[str],add]

def Node_1(state:CustomReducerState):
    print("node1接受收到了state")
    return {
        "count":state['count']+1,
        "nodes":['node_1']

            }

def Node_2(state:CustomReducerState):
    print("node2接受收到了state")
    return {
        "count":state['count']+1,
        "nodes":['node_2']
            }

graph_builder = StateGraph(CustomReducerState)
graph_builder.add_node("node_1", Node_1)
graph_builder.add_node("node_2", Node_2)
graph_builder.add_edge(START, "node_1")
graph_builder.add_edge("node_1", "node_2")
graph_builder.add_edge("node_2", END)

graph = graph_builder.compile()

result = graph.invoke({
    "count": 0,
    "nodes": []
})
print(result)
display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
