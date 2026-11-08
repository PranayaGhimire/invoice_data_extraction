
from datetime import date

from pydantic import BaseModel, Field


class InvoiceItem(BaseModel):
    description: str | None = None
    quantity: float | None = None
    unit: str | None = None
    unit_price: float | None = None
    line_total: float | None = None


class InvoiceSchema(BaseModel):
    invoice_number: str | None = None
    invoice_date: date | None = None
    supplier_name: str | None = None

    items: list[InvoiceItem] = Field(default_factory=list)

    subtotal: float | None = None
    tax_label: str | None = None
    tax_rate: float | None = None
    tax_amount: float | None = None
    total_amount: float | None = None
    currency: str | None = None
