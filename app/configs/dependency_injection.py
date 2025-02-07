from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine

from app.adapters.repositories.invoice import InvoiceRepository
from app.adapters.repositories.email import EmailRepository
from app.configs.settings import settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.adapters.entrypoints.invoice"],
    )

    config = providers.Configuration()
    config.from_dict(settings)

    db_engine = providers.Singleton(
        create_async_engine,
        str(settings.db_url),
        isolation_level="AUTOCOMMIT",
    )

    invoice_port = providers.Factory(InvoiceRepository, db_engine=db_engine)
    email_port = providers.Factory(EmailRepository, db_engine=db_engine)
