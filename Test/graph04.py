from typing import TypedDict, Annotated

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from rich.jupyter import display

from IPython.display import Image, display


def add(old,new):
    return old+new

class ParallelState(TypedDict):
    nodes: Annotated[list[str],add]

def Node_1(state:ParallelState):
    print(f"node1接受收到了state:{state}")
    return {
        "nodes":['a']

            }

def Node_2(state:ParallelState):
    print(f"node2接受收到了state:{state}")
    return {
        "nodes":['b']
            }
def Node_3(state:ParallelState):
    print(f"node3接受收到了state::{state}")
    return {
        "nodes":['c']
            }
def Node_4(state:ParallelState):
    print(f"node4接受收到了state:{state}")
    return {
        "nodes":['d']
            }

graph_builder = StateGraph(ParallelState)
graph_builder.add_node("node_1", Node_1)
graph_builder.add_node("node_2", Node_2)
graph_builder.add_node("node_3", Node_3)
graph_builder.add_node("node_4", Node_4)


graph_builder.add_edge(START, "node_1")
graph_builder.add_edge("node_1", "node_2")
graph_builder.add_edge("node_1", "node_3")
graph_builder.add_edge("node_2", "node_4")
graph_builder.add_edge("node_3", "node_4")

graph_builder.add_edge("node_4", END)
graph = graph_builder.compile()

result = graph.invoke({
    "nodes": []
})
print(result)
display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
