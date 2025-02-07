from sqlalchemy import Engine, text
from typing import List, Tuple, Set
from pydantic import ValidationError

from app.domain.models.invoice import Invoice
from app.domain.ports.invoice import InvoicePort


class InvoiceRepository(InvoicePort):

    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    async def bulk_save_invoices(self, invoices: List[Invoice]) -> Tuple[Invoice, Set] | None:  # noqa
        error_rows = set()
        processed_rows = []
        batch_lines = set()
        for row in invoices:
            try:
                row = Invoice.model_validate(row).model_dump()
            except ValidationError:
                error_rows.add(row)

            if len(batch_lines) < 50000:
                batch_lines.add(
                    f"('{row['name']}', '{row['governmentId']}', '{row['email']}', "
                    f"{row['debtAmount']}, '{row['debtDueDate']}', '{row['debtId']}', false)"
                )

            # just trying to avoid duplicated code
            if len(batch_lines) == 50000 or len(batch_lines) == len(invoices) - len(error_rows):

                async with self.db_engine.connect() as conn:
                    stmt = text(
                        f"""INSERT INTO invoices (name, governmentId, email, debtAmount, debtDueDate, debtId, generated)
                        VALUES {", ".join(batch_lines)}
                        ON CONFLICT DO NOTHING
                        RETURNING name, governmentId, email, debtAmount, debtDueDate, debtId
                        """  # NOQA
                    )
                    result = await conn.execute(stmt)
                    raw_invoices = result.fetchall()

                    if raw_invoices:
                        for raw_invoice in raw_invoices:
                            processed_rows.append(Invoice.model_validate({
                                "name": raw_invoice._mapping["name"],
                                "governmentId": raw_invoice._mapping["governmentid"],
                                "email": raw_invoice._mapping["email"],
                                "debtAmount": raw_invoice._mapping["debtamount"],
                                "debtDueDate": raw_invoice._mapping["debtduedate"],
                                "debtId": raw_invoice._mapping["debtid"]
                            }).model_dump())

                    batch_lines = set()

        return processed_rows, error_rows

    async def update_generated_invoices(self, invoice_ids: List[str]) -> List[Invoice] | None:  # noqa
        counter = 0
        batch_lines = set()
        for invoice_id in invoice_ids:
            if len(batch_lines) < 50000:
                batch_lines.add(f"'{invoice_id}'")

            # just trying to avoid duplicated code
            if len(batch_lines) == 50000 or len(batch_lines) == len(invoice_ids):

                async with self.db_engine.connect() as conn:
                    stmt = text(
                        f"""UPDATE invoices
                        SET generated = true
                        WHERE debtId IN ({', '.join(batch_lines)})
                        """  # noqa
                    )

                    result = await conn.execute(stmt)
                    counter += result.rowcount

                batch_lines = set()

        return counter

    async def set_invoice_emails_as_sent(self, invoice_ids: List[str]) -> List[Invoice] | None:  # noqa
        counter = 0
        batch_lines = set()
        for invoice_id in invoice_ids:
            if len(batch_lines) < 50000:
                batch_lines.add(f"'{invoice_id}'")

            # just trying to avoid duplicated code
            if len(batch_lines) == 50000 or len(batch_lines) == len(invoice_ids):
                async with self.db_engine.connect() as conn:
                    stmt = text(
                        f"""UPDATE invoices
                        SET email_sent = true
                        WHERE debtId IN ({', '.join(batch_lines)})
                        """  # noqa
                    )

                    result = await conn.execute(stmt)
                    counter += result.rowcount

                batch_lines = set()

        return counter
