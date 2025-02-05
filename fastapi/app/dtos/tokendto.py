# models.py
from pydantic import BaseModel
from typing import Optional

class TokenDto(BaseModel):
    username: str
    password: str
