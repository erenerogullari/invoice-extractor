from typing import TypedDict, List, Dict, Any, Optional
from src.schema.invoice import Invoice

class AgentState(TypedDict):
    """
    A dictionary representing the state of an agent.
    """
    pdf_path: str
    invoice_data: Optional[Invoice]
    errors: List[str]
    iteration_count: int