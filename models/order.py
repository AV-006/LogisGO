from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float
from sqlalchemy.orm import relationship
from .base import Base

class Order(Base):
    __tablename__="orders"
    id=Column(Integer, primary_key=True, index=True)
    status=Column(String, default="Pending")
    user_id=Column(Integer, ForeignKey("users.id"))
    supplier_id=Column(Integer, ForeignKey("suppliers.id"))
    user=relationship("User", back_populates="orders")
    items=relationship("OrderItem", back_populates="order")
    from_supplier=relationship("Supplier", back_populates="inc_order")
