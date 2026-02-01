import os
import sqlite3
from dotenv import load_dotenv
from src.agents.graph import app
from src.utils.ocr import extract_text_from_pdf
import logging

load_dotenv()

log = logging.getLogger(__name__)

def run_invoice_extraction(file_path: str):
    log.info(f"Starting the invoice agent.")
    initial_state = {
        "pdf_path": file_path, 
        "invoice_data": None,
        "errors": [],
        "iteration_count": 0
    }
    result = app.invoke(initial_state)
    log.info(f"Invoice agent result: {result}")

    # Display the final state of the database after insertion
    try:
        conn = sqlite3.connect("data/invoice.db")
        cursor = conn.cursor()
        
        # Print invoices table
        print("\nInvoices Table:")
        for row in cursor.execute("SELECT * FROM invoices"):
            print(row)
        
        print("\nLine Items Table:")
        for row in cursor.execute("SELECT * FROM line_items"):
            print(row)
        
        conn.close()
    except Exception as e:
        log.error(f"Error reading database: {e}")

if __name__ == "__main__":
    sample_invoice_path = "data/invoice-correct.pdf"
    run_invoice_extraction(sample_invoice_path)