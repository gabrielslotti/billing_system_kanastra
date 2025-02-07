from sqlalchemy import Engine, text

from app.domain.models.email import Email
from app.domain.ports.email import EmailPort


class EmailRepository(EmailPort):

    def __init__(self, db_engine: Engine):
        self.db_engine = db_engine

    async def save_email(self, debtId: str) -> Email | None:
        async with self.db_engine.connect() as conn:
            stmt = text(
                """INSERT INTO email (debtId, sent)
                VALUES (:debtId, true)
                """
            )
            stmt = stmt.bindparams(debtId=debtId)
            result = await conn.execute(stmt)
            raw_email = result.fetchone()

            if raw_email:
                return Email.model_validate(raw_email._mapping)

            return None
