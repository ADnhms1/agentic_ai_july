import json
import sqlite3
import uuid

from typing import Any, TypedDict

from fastapi import FastAPI, HTTPException
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver


# shared state

class SupportState(TypedDict, total=False):
    ticket: dict[str, Any]
    customer_data: dict[str, Any]
    category: str
    tool_results: dict[str, Any]
    internal_notes: list[str]
    sanitized_input: str
    final_response: str
    correction_audit: list[dict[str, Any]]


# mock external system

# intentionnaly stale crm response for the first incident.
CRM_CACHE = {
    "C-1002": {
        "status": "Past Due",
        "outstanding": 998,
        "source": "stale_cache"
    }
}

# verified source of truth
CRM_SOURCE_OF_TRUTH = {
    "C-1002": {
        "status": "Settled",
        "outstading": 0,
        "source": "verified_ledger"
    }
}

# simulate an actual crm lookup
def get_customer_details(customer_id: str) -> dict:
    return dict(CRM_CACHE.get(customer_id, {}))


# 3 graph nodes

def ingress_node(state: SupportState):
    ticket = state.get("ticket", {})
    return {
        "santized_input": ticket.get("message", ""),
        "internal_notes": ["Ticket recieved"],
    }

def classify_node(state: SupportState):
    message = state.get("sanitized_input", "").lower()

    category = (
        "billing" if any(
            word in message
            for word in ["bill", "payment", "paid", "refund", "invoice"]
        )
        else "technical"
    )

    return {"category": category}

def crm_tool_node(state: SupportState):
    ticket = state.get("ticket", {})
    customer_id = ticket.get("customer_id", "")

    customer_data = get_customer_details(customer_id)

    return {
        "customer_data": customer_data,
        "tool_result": {
            "crm_lookup": customer_data
        }
    }

def agent_node(state: SupportState):
    ticket = state.get("ticket", {})
    customer = state.get("customer_details", {})

    name = ticket.get("customer_name", "Customer")
    status = customer.get("status", "Unknown")
    amount = customer.get("outstanding", "Unknown")

    if status == "Settled":
        response = (
            f"Hi {name}, you account is settled. "
            "There is no outstanding amount."
        )
    elif status == "Past Due":
        response = (
            f"Hi {name}, our record show an outstanding"
            f"balance of Rs. {amount}. Please verify before paying."
        )
    else:
        response = (
            f"Hi {name}, we count not verify your account status"
            "Our support team will investigate."
        )

    return {
        "final_response": response
    }

# Build the graph

builder = StateGraph(SupportState)

builder.add_node("ingress_node", ingress_node)
builder.add_node("classify_node", classify_node)
builder.add_node("crm_tool_node", crm_tool_node)
builder.add_node("agent_node", agent_node)

builder.add_edge(START, "ingress_node")
builder.add_edge("ingress_node", "classify_node")
builder.add_edge("classify_node", "crm_tool_node")
builder.add_edge("crm_tool_node", "agent_node")
builder.add_edge("agent_node", END)

# keep the connection and checkpointer alive

conn = sqlite3.connect("forensics.sqlite", check_same_thread=False)

checkpointer = SqliteSaver(conn)
checkpointer.setup()

graph = builder.compile(checkpointer=checkpointer)

# helper to run a new ticket

def run_ticket(ticket : dict, thread_id: str | None = None) -> dict:
    thread_id = thread_id or str(uuid.uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id,
        }
    }

    result = graph.invoke(
        {"ticket": ticket},
        config=config
    )

    return {
        "thread_id": thread_id,
        "category": result.get("category"),
        "customer_data": result.get("customer_data"),
        "final_response": result.get("final_response")
    }

if __name__ == "__main__":
    result = run_ticket({
        "customer_id": "C-1002",
        "customer_name": "rupesh",
        "message": "I already paid my bill. Why is it showing due?"
    })

print(json.dumps(result, indent=2))