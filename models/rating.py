from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float, Enum
from sqlalchemy.orm import relationship
from .enums import OrderStatus
from .base import Base

class Rating(Base):
    __tablename__="ratings"
    id=Column(Integer, primary_key=True, index=True)
    rate=Column(Float, default=0.00)
    user_id=Column(Integer, ForeignKey("users.id"))
    supplier_id=Column(Integer, ForeignKey("suppliers.id"))
    supplier=relationship("Supplier", back_populates="rating")
    user=relationship("User", back_populates="rating")