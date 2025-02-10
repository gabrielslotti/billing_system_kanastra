import datetime
from unittest.mock import AsyncMock

import pytest
from starlette.testclient import TestClient

from app.configs.depency_injection import Container
from app.domain.models.invoice import Invoice
from app.domain.ports.invoice import InvoicePort
from app.main import app


INVOICE = {
    "name": "Gabriel Lotti",
    "governmentId": "1111111",
    "email": "gslotti.dev@gmail.com",
    "debtAmount": 1000.00,
    "debDueDate": "2025-03-09",
    "debtId": "abc"
}

@pytest.fixture
def invoice() -> Invoice:
    return Invoice(**INVOICE)


@pytest.fixture
async def mock_invoice_port(invoice):
    return AsyncMock(spec=InvoicePort,
                     bulk_save_invoices=AsyncMock(return_value=invoice),
                     update_generated_invoices=AsyncMock(return_value=invoice),
                     set_invoice_emails_as_sent=AsyncMock(return_value=invoice)
                     )


@pytest.fixture
def container(mocker, mock_invoice_port):
    container = Container()
    container.db_engine.override(mocker.Mock())
    container.invoice_port.override(mock_invoice_port)
    return container


@pytest.fixture
def client(container):
    app.container = container
    return TestClient(app)


def test_generate_invoices(client):
    # Given
    response = client.post("/generate_invoices")

    # Then
    assert response.status_code == 200
    assert response.json == {
	"total": 2,
        "processed": 2,
        "error": 0,
        "details": {"error": 0}
    }
