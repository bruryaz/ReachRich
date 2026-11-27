from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    account_id: str
    category_id: str | None = None
    transaction_type: Literal["income", "expense"]
    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    description: str | None = Field(default=None, max_length=255)
    transaction_date: date