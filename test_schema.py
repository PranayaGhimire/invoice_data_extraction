
from decimal import Decimal

from src.schemas import InvoiceSchema

invoice = InvoiceSchema(
    invoice_number="RT-2024-1052",
    supplier_name="RIVERTECH SUPPLIES LTD.",
    subtotal=Decimal("-100500"),
    tax_label="VAT",
    tax_rate=Decimal("13"),
    tax_amount=Decimal("13065"),
    total_amount=Decimal("113565"),
    currency="NPR",
)

print(invoice.model_dump_json(indent=2))
