#apart from updating or adding new parts, what else the supplier can do:
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from models import *
from schemas import *
from database import create_session
from oauth import get_current_user

router=APIRouter(tags=["Supplier"])
#view user profiles(both supplier and customer)

# @router.get('/user',response_model=ShowUser)
# def view_user(user_id:int,session: Session =Depends(create_session)):
#     user=session.query(User).filter(User.id==user_id).first()
#     if not user:
#         raise HTTPException(status_code=404,detail="User not found")
#     return user

@router.put('/accept')
def accept_order(order_id:int,session: Session =Depends(create_session),current_user: User=Depends(get_current_user)):
    if (current_user.role!="supplier"):
        raise HTTPException(status_code=404,detail="Not authenticated")
    user=session.query(Supplier).filter(Supplier.user_id==current_user.id).first()
    if not user:
        raise HTTPException(status_code=404,detail="Supplier not found")
    order=session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=404,detail="Order not found")
    setattr(order,"status","Accepted")
    session.commit()
    return order
#orders route
@router.get('/orders')
def incoming_orders(session: Session =Depends(create_session),current_user: User=Depends(get_current_user)):
    if (current_user.role!="supplier"):
        raise HTTPException(status_code=404,detail="Not authenticated")
    user=session.query(Supplier).filter(Supplier.user_id==current_user.id).first()
    if not user:
        raise HTTPException(status_code=404,detail="Supplier not found")
    orders=session.query(Order).filter(Order.supplier_id==current_user.id).all()
    if not orders:
        return {"No orders to be displayed"}
    return orders