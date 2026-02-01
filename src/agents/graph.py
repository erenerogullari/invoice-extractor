from sre_parse import State
from langgraph.graph import StateGraph, START, END
from src.agents.nodes import extract_from_pdf, validate_invoice_data, should_continue, save_to_database
from src.agents.state import AgentState
import logging

log = logging.getLogger(__name__)

log.info(f"Building the invoice agent workflow.")
workflow = StateGraph(AgentState)
workflow.add_node("extractor", extract_from_pdf)
workflow.add_node("validator", validate_invoice_data)
workflow.add_node("saver", save_to_database)
workflow.add_edge(START, "extractor")
workflow.add_edge("extractor", "validator")
workflow.add_conditional_edges(
    "validator",
    should_continue,
    {
        "re-extract": "extractor",
        "human_review": END,
        "end": "saver",
    }
)
workflow.add_edge("saver", END)

app = workflow.compile()

log.info(f"Generating the graph structure.")
with open("media/graph_structure.png", "wb") as f:
    f.write(app.get_graph().draw_mermaid_png())