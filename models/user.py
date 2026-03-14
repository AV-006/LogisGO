from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)
    email=Column(String, unique=True, nullable=False)
    password=Column(String, nullable=False)
    role=Column(String, default="customer")
    orders=relationship("Order", back_populates="user")
    supplier=relationship("Supplier", back_populates="user")
    rating=relationship("Rating", back_populates="user")