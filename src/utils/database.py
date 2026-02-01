import sqlite3
import logging

log = logging.getLogger(__name__)

def init_db():
    """
    Initializes the database.
    """
    log.info(f"Initializing the database.")
    conn = sqlite3.connect("data/invoice.db")
    cursor = conn.cursor()
    # Table for general invoice info
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_name TEXT,
            invoice_number TEXT,
            date TEXT,
            grand_total REAL
        )
    ''')
    # Table for specific items (linked to the invoice)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS line_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            description TEXT,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY(invoice_id) REFERENCES invoices(id)
        )
    ''')
    conn.commit()
    return conn


if __name__ == "__main__":
    init_db()