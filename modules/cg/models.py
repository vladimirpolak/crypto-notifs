from typing import List
from pydantic import BaseModel


class Price(BaseModel):
    currency: str
    value: float


class Coin(BaseModel):
    name: str
    symbol: str
    price: List[Price]
