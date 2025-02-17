from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class Stock(BaseModel):
    iventory_id: str
    quantity: Optional[int] = 0


class Price(BaseModel):
    channel_id: str
    currency: str
    amount: Decimal
    amount_discounted: Optional[Decimal] = None
