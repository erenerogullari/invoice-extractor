from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """
You are an expert financial auditor. Your task is to extract structured data from invoice text.
- Be precise with numbers.
- If a value is missing, do not guess; return null.
- Ensure the line item 'total' equals 'quantity * price'.
"""

EXTRACTION_PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", """
    Here is the invoice text:
    {raw_text}
    
    {error_instructions}
    
    Please extract the data into the required format.
    """)
])

def extraction_prompt(raw_text: str, errors: list = None):
    """Helper function to format the extraction prompt."""
    error_instructions = ""
    if errors:
        error_instructions = f"\nPrevious attempt had the following errors: {', '.join(errors)}. Please fix these errors and try again."
    
    return EXTRACTION_PROMPT.format_prompt(raw_text=raw_text, error_instructions=error_instructions)