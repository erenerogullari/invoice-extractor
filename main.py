import argparse
import sqlite3
from dotenv import load_dotenv
from src.agents.graph import app
import logging

load_dotenv()

log = logging.getLogger(__name__)

def run_invoice_extraction(*, pdf_path: str):
    log.info(f"Starting the invoice agent.")
    initial_state = {
        "pdf_path": pdf_path,
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
    parser = argparse.ArgumentParser(description="Extract structured data from an invoice PDF.")
    parser.add_argument(
        "--pdf-path",
        "-p",
        default="data/invoice-correct.pdf",
        help="Path to the invoice PDF (default: data/invoice-correct.pdf)",
    )
    args = parser.parse_args()
    run_invoice_extraction(pdf_path=args.pdf_path)