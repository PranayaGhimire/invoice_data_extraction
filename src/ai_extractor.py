
import mimetypes
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from pydantic import ValidationError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from src.schemas import InvoiceSchema


# --------------------------------------------------
# Configuration
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing. Check your .env file.")

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

client = genai.Client(api_key=API_KEY)


# --------------------------------------------------
# Extraction prompt
# --------------------------------------------------

EXTRACTION_PROMPT = """
You are an expert invoice data extraction system.

Analyze the provided invoice image and extract the information.

Extract the following fields:

1. Invoice number
2. Invoice date
3. Supplier name
4. Items:
   - Description
   - Quantity
   - Unit
   - Unit price
   - Line total
5. Subtotal
6. Tax label (e.g. VAT)
7. Tax rate
8. Tax amount
9. Total amount
10. Currency

Important instructions:

- Extract values exactly as shown in the invoice.
- Do not invent or guess missing information.
- Use null for missing or unreadable fields.
- Return invoice_date in YYYY-MM-DD format.
- Extract all invoice items.
- Do not calculate or modify invoice amounts.
- Preserve the original currency.
- Distinguish between subtotal, tax, and total amount.
"""


# --------------------------------------------------
# Gemini API
# --------------------------------------------------

@retry(
    retry=retry_if_exception_type(
        (ServerError, httpx.TransportError)
    ),
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(
        multiplier=1,
        min=2,
        max=10,
    ),
    reraise=True,
)
def generate_invoice_content(image_part: types.Part):
    return client.models.generate_content(
        model=MODEL,
        contents=[EXTRACTION_PROMPT, image_part],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=InvoiceSchema,
            temperature=0,
        ),
    )


# --------------------------------------------------
# Invoice extraction
# --------------------------------------------------

def extract_invoice(image_path: str | Path) -> InvoiceSchema:

    path = Path(image_path)

    # Validate file existence
    if not path.is_file():
        raise FileNotFoundError(
            f"Invoice image not found: {path}"
        )

    # Validate image MIME type
    mime_type, _ = mimetypes.guess_type(path.name)

    allowed_types = {
        "image/png",
        "image/jpeg",
        "image/webp",
    }

    if mime_type not in allowed_types:
        raise ValueError(
            f"Unsupported image format: {mime_type}"
        )

    try:
        # Read image
        image_bytes = path.read_bytes()

        if not image_bytes:
            raise ValueError("Invoice image is empty.")

        # Create Gemini image input
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type,
        )

        # Generate structured response
        response = generate_invoice_content(image_part)

        # Prefer SDK-parsed structured response
        if response.parsed is not None:
            return InvoiceSchema.model_validate(
                response.parsed
            )

        # Fallback to JSON parsing
        if response.text:
            return InvoiceSchema.model_validate_json(
                response.text
            )

        raise ValueError(
            "Gemini returned an empty response."
        )

    except ValidationError:
        raise

    except Exception as error:
        raise RuntimeError(
            f"Invoice extraction failed: {error}"
        ) from error
