from abc import ABC, abstractmethod

from app.domain.models.invoice import Invoice


class InvoicePort(ABC):

    async def bulk_save_invoices(self, invoice: Invoice) -> Invoice | None:
        pass

    async def update_generated_invoices(self, debtId: str) -> Invoice | None:
        pass

    async def set_invoice_emails_as_sent(self, debtId) -> Invoice | None:
        pass
