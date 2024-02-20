from pydantic import BaseModel
from decimal import Decimal

class CurrencyBase(BaseModel):
    name: str
    rate: Decimal

    class Config:
        orm_mode = True

class CreateCurrency(CurrencyBase):
    class Config:
        orm_mode = True