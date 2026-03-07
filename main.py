from fastapi import FastAPI
from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float
from sqlalchemy.orm import declarative_base,relationship     

Base=declarative_base()

class Supplier(Base):
    __tablename__="suppliers"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)
    content=Column(Text, nullable=False)
    parts=relationship("Parts", back_populates="supplier")
    rating=Column(Float, default=0.00)
    location=Column(String, nullable=False)


class Part(Base):
    __tablename__="parts"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)
    supplier_id=Column(Integer, ForeignKey("suppliers.id"))
    supplier=relationship("Supplier", back_populates="parts")


class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, nullable=False)
    age=Column(Integer, nullable=False)
    email=Column(String, nullable=False)
    password=Column(String, nullable=False)
    role=Column(String, default="Customer")
    orders=relationship("Orders", back_populates="user")

class Order(Base):
    __tablename__="orders"
    id=Column(Integer, primary_key=True, index=True)
    status=Column(String, default="Pending")
    user_id=Column(Integer, ForeignKey("users.id"))
    user=relationship("User", back_populates="orders")


app=FastAPI()