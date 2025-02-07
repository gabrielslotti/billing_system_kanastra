from abc import ABC, abstractmethod

from app.domain.models.email import Email


class EmailPort(ABC):

    @abstractmethod
    async def send_email(self, name: str, email: str) -> Email:
        pass
