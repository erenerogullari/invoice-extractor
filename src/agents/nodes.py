from src.agents.state import AgentState
from src.chains.extractor import structured_llm
from src.chains.prompts import get_extraction_instruction
from langchain.messages import HumanMessage
from src.schema.invoice import Invoice, invoice_to_df
from typing import TypedDict, List, Dict, Any, Optional
import sqlite3
import logging
import base64

log = logging.getLogger(__name__)

def extract_from_pdf(state: AgentState) -> Dict[str, Any]:
    """
    Extracts invoice data from a PDF file using Gemini's multimodality.
    """
    with open(state["pdf_path"], "rb") as file:
        pdf_data = base64.b64encode(file.read()).decode("utf-8")

    instruction_text = get_extraction_instruction(errors=state.get("errors") or [])
    message = HumanMessage(
        content=[
            {"type": "text", "text": instruction_text},
            {
                "type": "media",
                "mime_type": "application/pdf",
                "data": pdf_data,
            },
        ]
    )
    invoice_data = structured_llm.invoke([message])
    log.debug(f"Extracted invoice data:\n {invoice_to_df(invoice_data)}")
    
    return {
        "invoice_data": invoice_data,
        "errors": [],
        "iteration_count": state["iteration_count"] + 1,
    }


def validate_invoice_data(state: AgentState) -> Dict[str, Any]:
    """
    Validates the invoice data.
    """
    log.info(f"Validating the invoice data.")
    invoice_data = state["invoice_data"]
    errors = []

    if invoice_data is None:
        errors.append("No invoice data found.")
        return {
            "invoice_data": invoice_data,
            "errors": errors,
            "iteration_count": state["iteration_count"] + 1,
        }
    line_totals = [item.price * item.quantity for item in invoice_data.line_items]
    log.debug(f"Line totals: {line_totals}")
    subtotal = sum(line_totals)
    tax_rate = invoice_data.tax_rate
    calculated_tax = subtotal * tax_rate
    calculated_total = (subtotal + calculated_tax)
    actual_total = invoice_data.grand_total

    if round(calculated_total, 2) != round(actual_total, 2):
        errors.append(
            f"Math mismatch: Line items + tax = {calculated_total}, "
            f"but invoice says {actual_total}"
        )
        log.info(f"Math mismatch: Line items + tax = {calculated_total}, but invoice says {actual_total}")

    log.debug(f"Errors: {errors}")
    
    return {
        "errors": errors, 
        "iteration_count": state["iteration_count"] + 1
    }


def should_continue(state: AgentState) -> str:
    """
    Determines if the agent should continue or ask for human intervention.
    """
    log.info(f"Determining if the agent should continue or ask for human intervention.")

    if not state["errors"]:
        return "end"
    elif state["iteration_count"] > 3:
        # Stop after 3 tries to prevent infinite loops (and high API costs!)
        log.info(f"Please review the invoice data and correct the errors.")
        return "human_review"
    else:
        log.info(f"Retrying extraction with error feedback.")
        return "re-extract"


def save_to_database(state: AgentState):
    """Saves the verified invoice data into the SQLite database."""
    log.info(f"Saving the invoice data to the database.")
    invoice = state["invoice_data"]
    
    conn = sqlite3.connect("data/invoice.db")
    cursor = conn.cursor()
    
    # 1. Insert main invoice record
    cursor.execute(
        """
        INSERT INTO invoices (vendor_name, invoice_number, date, grand_total)
        VALUES (?, ?, ?, ?)
        """,
        (
            invoice.customer_company,
            invoice.invoice_number,
            invoice.invoice_date.isoformat(),
            invoice.grand_total,
        ),
    )
    invoice_id = cursor.lastrowid
    
    # 2. Insert line items
    for item in invoice.line_items:
        cursor.execute(
            """
            INSERT INTO line_items (invoice_id, description, quantity, price)
            VALUES (?, ?, ?, ?)
            """,
            (
                invoice_id,
                item.description,
                item.quantity,
                item.price,
            ),
        )
    
    conn.commit()
    conn.close()
    return {"errors": []} # Final step, no more errors