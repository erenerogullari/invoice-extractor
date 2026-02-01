# Invoice Extractor

An AI-powered invoice extraction tool that uses LangGraph and Google's Gemini model to parse PDF invoices into structured data and persist it to SQLite. PDFs are sent directly to Gemini via its multimodal API—no separate OCR step is required.

## How It Works

The application uses a multi-step agent workflow. The PDF is sent directly to Gemini; no separate OCR step is used—Gemini's multimodality handles reading the invoice PDF and extracting structured data.

1. **Extract** — The PDF is passed to Gemini as multimodal input; the model reads the document and returns structured data matching the `Invoice` schema.
2. **Validate** — Checks data consistency (e.g. line item totals, grand total).
3. **Retry or Save** — On validation errors, the agent re-extracts with error feedback; otherwise saves to the database. After several retries, the workflow can route to human review.

Workflow diagram:

![Invoice extraction workflow](media/graph_structure.png)

## Prerequisites

- **Python 3.10+**
- **Google AI API key** — Get one at [Google AI Studio](https://makersuite.google.com/app/apikey)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/erenerogullari/invoice-extractor
cd invoice-extractor
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_api_key_here
```

> **Note:** Never commit `.env` — it is already listed in `.gitignore`.

## Running Locally

From the project root, run with the path to your invoice PDF:

```bash
python main.py --pdf-path path/to/your/invoice.pdf
```

Short form:

```bash
python main.py -p path/to/your/invoice.pdf
```

If you omit the path, the default sample invoice is used:

```bash
python main.py
# Uses data/invoice-correct.pdf
```

You can also call the extractor from Python with the PDF path as a keyword argument:

```python
from main import run_invoice_extraction

run_invoice_extraction(pdf_path="path/to/your/invoice.pdf")
```

## Project Structure

```
invoice-extractor/
├── main.py                 # Entry point
├── requirements.txt
├── data/
│   ├── invoice-correct.pdf # Sample invoice
│   ├── invoice-wrong.pdf   # Another sample
│   └── invoice.db          # SQLite database (created on first run)
├── media/
│   └── graph_structure.png # Workflow diagram
└── src/
    ├── agents/             # LangGraph workflow
    │   ├── graph.py        # Graph definition
    │   ├── nodes.py        # Extract, validate, save nodes
    │   └── state.py        # Agent state
    ├── chains/
    │   ├── extractor.py    # LLM setup (Gemini)
    │   └── prompts.py      # Extraction prompts
    ├── schema/
    │   └── invoice.py      # Pydantic models
    └── utils/
        └── database.py     # SQLite helpers
```

## Output

On success, the script prints:

- Extracted invoice fields (number, dates, customer, line items, totals)
- Contents of the `invoices` and `line_items` tables in `data/invoice.db`
