from fastapi import FastAPI
from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float
from sqlalchemy.orm import declarative_base,relationship     

Base=declarative_base()

class Supplier(Base):
    __tablename__="suppliers"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)
    description=Column(Text, nullable=False)
    parts=relationship("Part", back_populates="supplier")
    rating=Column(Float, default=0.00)
    location=Column(String, nullable=False)


class Part(Base):
    __tablename__="parts"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)
    description=Column(Text)
    price=Column(Float, nullable=False)
    car_model=Column(String, nullable=False)
    stock=Column(Integer, default=0)

    supplier_id=Column(Integer, ForeignKey("suppliers.id"))
    supplier=relationship("Supplier", back_populates="parts")


class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)
    email=Column(String, unique=True, nullable=False)
    password=Column(String, nullable=False)
    role=Column(String, default="Customer")
    orders=relationship("Order", back_populates="user")

class Order(Base):
    __tablename__="orders"
    id=Column(Integer, primary_key=True, index=True)
    status=Column(String, default="Pending")
    user_id=Column(Integer, ForeignKey("users.id"))
    user=relationship("User", back_populates="orders")
    items=relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__="order_items"
    id=Column(Integer, primary_key=True, index=True)
    order_id=Column(Integer, ForeignKey("orders.id"))
    parts_id=Column(Integer, ForeignKey("parts.id"))
    order=relationship("Order",back_populates="items")

    

class Complaint(Base):
    __tablename__="complaints"
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    status=Column(String, default="Unresolved")


app=FastAPI()