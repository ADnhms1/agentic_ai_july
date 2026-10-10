from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class WorkflowState(TypedDict, total=False):
    request: str
    category: str
    response: str

def classify(state: WorkflowState):
    text = state["request"].lower()

    if "payment" in text or "refund" in text:
        return {"category": "billing"}
    
    return {"category": "tech"}

# graph

triage_builder = StateGraph(WorkflowState)
triage_builder.add_node("classify", classify)

triage_builder.add_edge(START, "classify")
triage_builder.add_edge("classify", END)

triage_subgraph = triage_builder.compile()

def billing_specialist(state: WorkflowState):
    return {"response": (
        "Billing team: investigate the payment reference"
    )}

def tech_specialist(state: WorkflowState):
    return {"response": (
        "Tech team: investigate the technical issue"
    )}

def route(state: WorkflowState):
    return state["category"]
    
master = StateGraph(WorkflowState)
master.add_node("triage", triage_subgraph)
master.add_node("billing", billing_specialist)
master.add_node("tech", tech_specialist)


master.add_edge(START, "triage")
master.add_conditional_edges("triage", route, {"billing": "billing", "tech": "tech"})
master.add_edge("billing", END)
master.add_edge("tech", END)

app = master.compile()

result = app.invoke({"request": "My app crashed when i open the application."})

print(result)  # Should route to tech_specialist