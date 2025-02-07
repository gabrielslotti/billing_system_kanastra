from datetime import date

from pydantic import BaseModel


class Invoice(BaseModel):
    name: str
    governmentId: str
    email: str
    debtAmount: float
    debtDueDate: date
    debtId: str
