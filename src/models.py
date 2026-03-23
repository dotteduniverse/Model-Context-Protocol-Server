from pydantic import BaseModel
from typing import Optional, List

class Order(BaseModel):
    id: int
    customer_name: str
    total: float

class Customer(BaseModel):
    id: int
    name: str
    email: str