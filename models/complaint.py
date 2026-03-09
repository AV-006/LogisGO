from sqlalchemy import Column,Integer,String,ForeignKey
from .base import Base

class Complaint(Base):
    __tablename__="complaints"
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey("users.id"))
    status=Column(String, default="Unresolved")
