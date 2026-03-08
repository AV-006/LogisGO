from sqlalchemy import Column,Integer,String,Text,ForeignKey,Float
from sqlalchemy.orm import declarative_base,relationship
     

Base=declarative_base()

class Complaint(Base):
    __tablename__="complaints"
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    status=Column(String, default="Unresolved")
