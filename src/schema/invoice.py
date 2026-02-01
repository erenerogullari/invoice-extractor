from typing import List
from pydantic import BaseModel, Field
from datetime import date
import pandas as pd

class LineItem(BaseModel):
    description: str = Field(description="The description of the line item.")
    price: float = Field(description="The unit price of the line item.")
    quantity: float = Field(description="The quantity of the line item.")
    total: float = Field(description="The total price of the line item (qty * unit_price).")

class Invoice(BaseModel):
    invoice_number: str = Field(description="The invoice number.")
    invoice_date: date = Field(description="The date of the invoice.")
    customer_name: str = Field(description="The name of the customer.")
    customer_company: str = Field(description="The company of the customer.")
    customer_email: str = Field(description="The email of the customer.")
    due_date: date = Field(description="The due date of the invoice.")
    line_items: List[LineItem] = Field(description="The line items of the invoice.")
    subtotal: float = Field(description="The subtotal of the invoice (sum of all line items).")
    tax_rate: float = Field(description="The tax rate of the invoice.")
    tax_amount: float = Field(description="The tax amount of the invoice (subtotal * tax_rate).")
    grand_total: float = Field(description="The grand total of the invoice (subtotal + tax_amount).")


def invoice_to_df(invoice: Invoice) -> pd.DataFrame:
    """Converts the invoice data to a pandas DataFrame."""
    return pd.DataFrame([item.model_dump() for item in invoice.line_items])