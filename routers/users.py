#apart from updating or adding new parts, what else the supplier can do:
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from models import *
from schemas import *
from database import create_session
from typing import Optional
from oauth import get_current_user

router=APIRouter(tags=["Users"])
#view user profiles(both supplier and customer)

@router.get('/user',response_model=ShowUser)
def view_user(user_id:int,session: Session =Depends(create_session)):
    user=session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.post('/order')
def place_order(order_item:PlaceOrder,session: Session =Depends(create_session),current_user: User=Depends(get_current_user)):
    order=Order(
        user_id=current_user.id,
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

@router.post('/complaint')
def post_complaint(complaint: PostComplaint, session: Session=Depends(create_session),current_user: User=Depends(get_current_user)):
    user_complaint=Complaint(
        complaint=complaint.complaint
    )
    session.add(user_complaint)
    session.commit()
    session.refresh(user_complaint)
    return user_complaint

@router.post('/rate')
def rate_supplier(rating: CreateRating, supplier_id: int,session: Session=Depends(create_session),current_user: User=Depends(get_current_user)):
    supplier=session.query(Supplier).filter(Supplier.id==supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404,detail="Supplier not found")
    existing_rating=session.query(Rating).filter(
        Rating.user_id==current_user.id,
        Rating.supplier_id==supplier_id
    ).first()

    if existing_rating:
        existing_rating.rate=rating.rating
        session.commit()
        return {"message":"Rating Updated"}
    
    new_rating=Rating(
        rate=rating.rating,
        user_id=current_user.id,
        supplier_id=supplier_id
    )

    session.add(new_rating)
    session.commit()
    session.refresh(new_rating)
    return {"message":"New rating created"}

@router.get('/ratings')
def get_supplier_ratings( supplier_id: int,session: Session=Depends(create_session),current_user: User=Depends(get_current_user)):
    supplier=session.query(Supplier).filter(Supplier.id==supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404,detail="Supplier not found")
    avg_ratings=session.query(func.avg(Rating.rate)).filter(
        Rating.supplier_id==supplier_id
    ).scalar()
    total_reviews=session.query(Rating).filter(
        Rating.supplier_id==supplier_id
    ).count()
    return {
        "supplier_id": supplier_id,
        "average_rating": round(avg_ratings, 2) if avg_ratings else 0,
        "total_reviews": total_reviews
    }