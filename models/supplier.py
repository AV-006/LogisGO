from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float
from sqlalchemy.orm import declarative_base,relationship
     

Base=declarative_base()

class Supplier(Base):
    __tablename__="suppliers"
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    name=Column(String, nullable=False)
    description=Column(Text)
    parts=relationship("Part", back_populates="supplier")
    rating=Column(Float, default=0.00)
    location=Column(String, nullable=False)
    user=relationship("User", back_populates="supplier")