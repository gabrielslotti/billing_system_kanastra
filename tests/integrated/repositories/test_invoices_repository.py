import datetime

import pytest

from app.adapters.repositories.invoice import InvoiceRepository
from app.domain.models.invoice import Invoice


@pytest.mark.asyncio
async def test_bulk_save_invoices(async_engine):
    # When
    invoice_port = InvoiceRepository(async_engine)

    # Given
    invoice = Invoice()

    persited_invoice = await invoice_port.bulk_save_invoices(invoice)

    # Then
    assert persited_invoice.id is not None
    assert persited_invoice.name == invoice.name
    assert persited_invoice.author == invoice.author
    assert persited_invoice.isbn == invoice.isbn
    assert persited_invoice.created_at == invoice.created_at


@pytest.mark.asyncio
async def test_update_invoice(async_engine):

    # When
    invoice_port = InvoiceRepository(async_engine)

    # Given
    invoice = Invoice(name="Test Invoice",
                author="Augusto Marinho",
                created_at=datetime.datetime.now(tz=datetime.timezone.utc),
                isbn="1234567890")

    persited_invoice = await invoice_port.create_invoice(invoice)
    persited_invoice.author = "Augusto Marinho 2"

    updated_invoice = await invoice_port.update_invoice(persited_invoice)

    # Then
    assert updated_invoice.id is not None
    assert updated_invoice.name == persited_invoice.name
    assert updated_invoice.author == persited_invoice.author
    assert updated_invoice.isbn == persited_invoice.isbn
    assert updated_invoice.created_at == persited_invoice.created_at
    assert updated_invoice.updated_at is not None


@pytest.mark.asyncio
async def test_get_invoice_by_id(async_engine):
    # When
    invoice_port = InvoiceRepository(async_engine)

    # Given
    invoice = Invoice(name="Test Invoice",
                author="Augusto Marinho",
                created_at=datetime.datetime.now(tz=datetime.timezone.utc),
                isbn="1234567890")

    persited_invoice = await invoice_port.create_invoice(invoice)
    readed_invoice = await invoice_port.get_invoice_by_id(persited_invoice.id)

    # Then
    assert readed_invoice.id is not None
    assert readed_invoice.name == persited_invoice.name
    assert readed_invoice.author == persited_invoice.author
    assert readed_invoice.isbn == persited_invoice.isbn
    assert readed_invoice.created_at == persited_invoice.created_at
    assert readed_invoice.updated_at is Nonev


@pytest.mark.asyncio
async def test_get_delete_invoice_by_id(async_engine):
    # When
    invoice_port = InvoiceRepository(async_engine)

    # Given
    invoice = Invoice(name="Test Invoice",
                author="Augusto Marinho",
                created_at=datetime.datetime.now(tz=datetime.timezone.utc),
                isbn="1234567890")

    persited_invoice = await invoice_port.create_invoice(invoice)
    await invoice_port.delete_invoice(persited_invoice.id)
    readed_invoice = await invoice_port.get_invoice_by_id(persited_invoice.id)

    # Then
    assert readed_invoice is None
