#apart from updating or adding new parts, what else the supplier can do:
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from models import *
from schemas import *
from database import create_session
from typing import Optional

router=APIRouter(tags=["Users"])
#view user profiles(both supplier and customer)

@router.get('/user',response_model=ShowUser)
def view_user(user_id:int,session: Session =Depends(create_session)):
    user=session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.post('/order')
def place_order(user_id:int,order_item:PlaceOrder,session: Session =Depends(create_session)):
    order=Order(
        user_id=user_id,
    )
    session.add(order)
    session.commit()
    session.refresh(order)
    
    orderitem=OrderItem(
        order_id=order.id,
        parts_id=order_item.parts_id
    )
    
    session.add(orderitem)
    session.commit()
    session.refresh(orderitem)
    return {"message":"order placed"}