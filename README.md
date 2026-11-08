# AI-Powered Invoice Data Extraction

A Python application that uses Google's Gemini AI to extract structured information from invoice images and return validated JSON data.

## 1. Overview

This application reads an invoice image, processes it using the Gemini API, and extracts important invoice information into a structured JSON format.

The extracted information includes:

- Invoice number
- Invoice date
- Supplier name
- Invoice items (description, quantity, unit, unit price, and line total)
- Subtotal
- Tax label and tax rate
- Tax amount
- Total amount
- Currency

The application also performs basic validation to check whether the extracted invoice calculations are consistent.

## 2. Technologies Used

- **Python** – Core application
- **Google Gemini API** – AI-powered invoice data extraction
- **Pydantic** – Structured data validation
- **HTTPX** – HTTP client for API communication
- **Tenacity** – Retry handling for temporary API and network failures
- **python-dotenv** – Environment variable management

## 3. Project Structure

```text
invoice-extractor/
│
├── src/
│   ├── __init__.py
│   ├── ai_extractor.py
│   ├── schemas.py
│   └── validator.py
│
├── invoices/
│   └── sample-invoice.png
│
├── test_extraction.py
├── test_gemini.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 4. Prerequisites

Before running the application, make sure you have:

- Python 3.10 or later
- A Google Gemini API key

You can obtain an API key from [Google AI Studio](https://aistudio.google.com/apikey).

## 5. Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/PranayaGhimire/invoice_data_extraction.git
cd invoice-extractor
```

### Step 2: Create a virtual environment

**Windows:**

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

```env
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_GENAI_HTTP_CLIENT=httpx
```

Replace `your_gemini_api_key` with your actual Gemini API key.

**Important:** Never commit your actual `.env` file or expose your API key publicly.

## 6. Running the Application

Place your invoice image inside the `invoices/` directory.

Update the image path in `test_extraction.py` if necessary.

Run the extraction:

```bash
python test_extraction.py
```

The application will:

1. Validate the invoice image path and supported format.
2. Read the image and convert it into Gemini-compatible input.
3. Send the image and extraction prompt to Gemini.
4. Receive structured JSON output.
5. Validate the extracted data using Pydantic.
6. Perform basic invoice calculation validation.
7. Display the extracted invoice information and validation results.

### Supported Image Formats

- PNG
- JPEG / JPG
- WEBP

## 7. Invoice Validation

The application performs basic business-rule validation.

**Subtotal validation:**

Checks whether the sum of the extracted item line totals matches the invoice subtotal.

**Total amount validation:**

Checks whether:

```text
Subtotal + Tax Amount = Total Amount
```

If a calculation does not match, the validator reports the discrepancy.

The validation also accounts for missing values by skipping checks that cannot be reliably performed.

## 8. Example Output

For the provided sample invoice, the application successfully extracts:

```json
{
  "invoice_number": "RT-2024-1052",
  "invoice_date": "2024-10-14",
  "supplier_name": "RIVERTECH SUPPLIES LTD.",
  "subtotal": 100500.0,
  "tax_label": "VAT",
  "tax_rate": 13.0,
  "tax_amount": 13065.0,
  "total_amount": 113565.0,
  "currency": "NPR"
}
```

The application also extracts all five invoice line items.

**Validation Result:**

```text
All invoice calculations are valid.
```

## 9. Error Handling

The application handles common errors, including:

- Missing invoice image
- Unsupported image formats
- Empty image files
- Missing Gemini API key
- Gemini API failures
- Temporary network errors
- Invalid or empty AI responses
- Structured data validation errors

Temporary API and network failures are handled using retry logic with exponential backoff.

## 10. Notes

- Extraction accuracy depends on invoice image quality and readability.
- Missing or unreadable invoice fields are represented as null where supported by the schema.
- Pydantic validates the response structure, while business-rule validation checks invoice calculations.
- AI-extracted information should be reviewed before being used for financial or accounting decisions.

---

**Developed as part of the AI-Powered Invoice Data Extraction practical assignment.**