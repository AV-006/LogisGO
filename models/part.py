from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float
from sqlalchemy.orm import declarative_base,relationship
     

Base=declarative_base()
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