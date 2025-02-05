# models.py
from pydantic import BaseModel
from typing import Optional

class ItemDto(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
