
from decimal import Decimal

from src.schemas import InvoiceSchema


def validate_invoice(invoice: InvoiceSchema) -> list[str]:
    errors = []

    # 1. Validate item line totals against subtotal
    if invoice.subtotal is not None and invoice.items:

        # Only perform this check when every line total is available.
        if all(item.line_total is not None for item in invoice.items):

            calculated_subtotal = sum(
                (Decimal(str(item.line_total)) for item in invoice.items),
                Decimal("0"),
            )

            expected_subtotal = Decimal(str(invoice.subtotal))

            if abs(calculated_subtotal - expected_subtotal) > Decimal("0.01"):
                errors.append(
                    f"Item totals ({calculated_subtotal}) "
                    f"do not match subtotal ({expected_subtotal})."
                )

    # 2. Validate subtotal + tax = total
    if (
        invoice.subtotal is not None
        and invoice.tax_amount is not None
        and invoice.total_amount is not None
    ):
        calculated_total = (
            Decimal(str(invoice.subtotal))
            + Decimal(str(invoice.tax_amount))
        )

        expected_total = Decimal(str(invoice.total_amount))

        if abs(calculated_total - expected_total) > Decimal("0.01"):
            errors.append(
                f"Subtotal + tax ({calculated_total}) "
                f"does not match total ({expected_total})."
            )

    return errors
