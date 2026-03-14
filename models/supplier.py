from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float
from sqlalchemy.orm import relationship
from .base import Base

class Supplier(Base):
    __tablename__="suppliers"
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    name=Column(String, nullable=False)
    description=Column(Text)
    parts=relationship("Part", back_populates="supplier")
    rating=relationship("Rating", back_populates="supplier")
    location=Column(String, nullable=False)
    user=relationship("User", back_populates="supplier")
    inc_order=relationship("Order", back_populates="from_supplier")