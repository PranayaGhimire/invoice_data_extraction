
from src.ai_extractor import extract_invoice
from src.validator import validate_invoice

invoice = extract_invoice(
    "invoices/sample-invoice.png"
)

print("\n===== EXTRACTED INVOICE =====\n")

print(invoice.model_dump_json(indent=2))

print("\n===== VALIDATION =====\n")

errors = validate_invoice(invoice)

if errors:
    print("Invoice validation failed:")

    for error in errors:
        print(f"- {error}")

else:
    print("All invoice calculations are valid.")