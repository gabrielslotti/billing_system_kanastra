from dependency_injector.wiring import Provide, inject
from fastapi import Response, status, APIRouter, UploadFile, Depends
from io import StringIO
import csv

from app.domain.models.invoice import Invoice
from app.domain.ports.invoice import InvoicePort
from app.configs.dependency_injection import Container

router = APIRouter()


@router.post("/generate_invoices")
@inject
async def generate_invoices(
    csv_file: UploadFile,
    invoice_port: InvoicePort = Depends(Provide[Container.invoice_port])
):
    print(f"Reading {csv_file.filename}...")

    try:
        content = await csv_file.read()
        decoded_content = content.decode('utf-8')
        csv_reader = csv.DictReader(StringIO(decoded_content), delimiter=',')

        print(f"Uploading {csv_file.filename}...")
        invoices = [Invoice(**row).model_dump() for row in csv_reader]
        processed_invoices, error_rows = await invoice_port.bulk_save_invoices(invoices)  # noqa

        print(f"Generating invoices of {csv_file.filename}...")
        invoice_ids = set([row['debtId'] for row in processed_invoices])
        await invoice_port.update_generated_invoices(invoice_ids)

        print(f"Sending invoice emails of {csv_file.filename}")
        await invoice_port.set_invoice_emails_as_sent(invoice_ids)

        return {
            "total": len(invoices),
            "processed": len(processed_invoices),
            "error": len(error_rows),
            "details": {"error": error_rows}
        }
    except Exception as exc:
        import traceback
        print(traceback.format_exc())
        print(str(exc))
        raise exc
