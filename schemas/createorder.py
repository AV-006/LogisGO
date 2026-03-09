from pydantic import BaseModel
from typing import List

class PlaceOrder(BaseModel):
    parts_id: int
    
