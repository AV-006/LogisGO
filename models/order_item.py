from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float
from sqlalchemy.orm import relationship
from .base import Base

class OrderItem(Base):
    __tablename__="order_items"
    id=Column(Integer, primary_key=True, index=True)
    order_id=Column(Integer, ForeignKey("orders.id"))
    parts_id=Column(Integer, ForeignKey("parts.id"))
    order=relationship("Order",back_populates="items")