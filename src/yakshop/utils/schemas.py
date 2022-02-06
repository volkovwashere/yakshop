from pydantic import BaseModel
from typing import Optional, List


class YakStock(BaseModel):
    milk: float
    wool: int


class Yak(BaseModel):
    name: str
    age: float
    age_last_shaved: Optional[float]


class Herd(BaseModel):
    herd: List[Yak]


class YakOrder(BaseModel):
    customer: str
    order: YakStock
