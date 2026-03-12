from pydantic import BaseModel
from models.enums import OrderStatus

class UpdateOrderStatus(BaseModel):
    status: OrderStatus