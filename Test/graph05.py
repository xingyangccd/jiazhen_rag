from typing import TypedDict, Annotated, Literal

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from rich.jupyter import display

from IPython.display import Image, display


def add(old,new):
    return old+new

class ScoreState(TypedDict):
    score:int
    result:str

def score_Node(state:ScoreState):
    score=input("请输入用户分数")
    return {
        "score": int(score)

            }

def Success_node(state:ScoreState):
    print(f"node2接受收到了state:{state}")
    return {
        "result":["恭喜考试通过"]
            }
def fail_node(state:ScoreState):
    print(f"node3接受收到了state::{state}")
    return {
          "result":["节哀，考试没通过"]
            }



graph_builder = StateGraph(ScoreState)
graph_builder.add_node("node_1", score_Node)
graph_builder.add_node("node_2", Success_node)
graph_builder.add_node("node_3", fail_node)


def router(state:ScoreState)->Literal["node_2", "node_3"]:
    if state["score"]>=60:
        return "node_2"
    else:
        return "node_3"

graph_builder.add_edge(START, "node_1")
graph_builder.add_conditional_edges("node_1",router)

graph_builder.add_edge("node_2", END)
graph_builder.add_edge("node_3", END)
graph = graph_builder.compile()

result = graph.invoke({
    "nodes": []
})
print(result)
display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
