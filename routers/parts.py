from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from models.part import Part
from models.supplier import Supplier
from models.user import User
from database import create_session
from schemas.createpart import CreatePart 
from typing import Optional
from oauth import get_current_user

router=APIRouter(tags=["Parts"])

@router.get('/parts')
def get_all_parts(session: Session =Depends(create_session)):
    parts=session.query(Part).all()
    return parts

@router.post('/parts/{supplier_id}')
def update_parts(part:CreatePart,session: Session =Depends(create_session), current_user: User=Depends(get_current_user)):
    if (current_user.role!="supplier"):
        raise HTTPException(status_code=404,detail="Not authenticated")
    user=session.query(Supplier).filter(Supplier.user_id==current_user.id).first()
    if not user:
        raise HTTPException(status_code=404,detail="Supplier not found")
    newPart=Part(
        name=part.name,
        description=part.description,
        price=part.price,
        car_model=part.car_model,
        stock=part.stock,
        supplier_id=user.id
    )
    session.add(newPart)
    session.commit()
    session.refresh(newPart)
    return newPart



#task: try to do search engine optimiztion(even if they type spark plug 'sparkplug' should be displayed)


@router.get('/parts/search')
def get_specific_part(car_model:Optional[str]=None,name:Optional[str]=None,session: Session=Depends(create_session)):
    query=session.query(Part)
    if name:
        query=query.filter(Part.name.ilike(f"%{name}%"))
    if car_model:
        query=query.filter(Part.car_model.ilike(f"%{car_model}%"))
    
    parts=query.all()
    
    return parts
    

@router.put('/parts/{supplier_id}/{part_id}')
def update_existing_parts(parts:CreatePart,part_id:int, session: Session =Depends(create_session),current_user: User=Depends(get_current_user)):
    if (current_user.role!="supplier"):
        raise HTTPException(status_code=404,detail="Not authenticated")
    user=session.query(Supplier).filter(Supplier.user_id==current_user.id).first()
    if not user:
        raise HTTPException(status_code=404,detail="Supplier not found")
    get_part=session.query(Part).filter(Part.id==part_id).first()
    for key,value in dict(parts).items():
        setattr(get_part,key,value)
    setattr(get_part,"supplier_id",user.id)
    session.commit()
    return dict(parts)

@router.delete('/parts/{supplier_id}/{part_id}')
def delete_parts(supplier_id: int,part_id:int,session: Session=Depends(create_session),current_user: User=Depends(get_current_user)):
    if (current_user.role!="supplier"):
        raise HTTPException(status_code=404,detail="Not authenticated")
    user=session.query(Supplier).filter(Supplier.user_id==current_user.id).first()
    if not user:
        raise HTTPException(status_code=404,detail="Supplier not found")
    get_part=session.query(Part).filter(Part.id==part_id).first()
    session.delete(get_part)
    session.commit()
    return {"message":"part deleted"}