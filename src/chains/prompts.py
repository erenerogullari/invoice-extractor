SYSTEM_PROMPT = """
You are an expert financial auditor. Your task is to extract structured data from the attached invoice PDF.
- Be precise with numbers.
- If a value is missing, do not guess; return null.
- Ensure the line item 'total' equals 'quantity * price'.
"""

EXTRACTION_HUMAN_TEMPLATE = """Extract structured data from the attached invoice PDF and return it in the required format.

{error_instructions}"""


def get_extraction_instruction(errors: list = None) -> str:
    """
    Returns the full instruction text for the extraction LLM call.
    Use this as the text part of a multimodal message; attach the PDF as media separately.
    """
    error_instructions = ""
    if errors:
        error_instructions = (
            "Previous attempt had the following errors: "
            + ", ".join(errors)
            + ". Please fix these errors and try again."
        )
    return SYSTEM_PROMPT.strip() + "\n\n" + EXTRACTION_HUMAN_TEMPLATE.format(
        error_instructions=error_instructions
    ).strip()
