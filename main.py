from datetime import timedelta
from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import Base,User,Part,Supplier
from database import engine,create_session
from schemas import UserCreate,Token,CreatePart
from hashing import password_hash,DUMMY_HASH
from auth_token import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES

app=FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/')
def main_page():
    return {"message":"Hello"}

@app.post('/auth/signup')
def create_user(user:UserCreate,session:Session=Depends(create_session)):
    if (session.query(User).filter(User.email==user.email).first()):
        raise HTTPException(status_code=400,detail="User already exists")
    hashed_password=password_hash.hash(user.password)
    new_user=User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )    
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    if user.role=="supplier":
        new_supplier=Supplier(
        user_id=new_user.id,
        name=user.name,
        location=user.location
    )
        session.add(new_supplier)
        session.commit()
        session.refresh(new_supplier)

    return {"message": "user created"}


#login route
@app.post('/auth/login')
def login_user(session: Session =Depends(create_session), form_data: OAuth2PasswordRequestForm = Depends()):
    user=session.query(User).filter(form_data.username==User.email).first()
    if not user:
        password_hash.verify(form_data.password,DUMMY_HASH)
        return {"message": "Invalid login credentials"} 
    if not password_hash.verify(form_data.password,user.password):
        return {"message": "Invalid login credentials"}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.get('/parts')
def get_all_parts(session: Session =Depends(create_session)):
    parts=session.query(Part).all()
    return parts

@app.post('/parts/{supplier_id}')
def update_parts(supplier_id : int,part:CreatePart,session: Session =Depends(create_session)):
    user=session.query(Supplier).filter(Supplier.id==supplier_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="Supplier not found")
    newPart=Part(
        name=part.name,
        description=part.description,
        price=part.price,
        car_model=part.car_model,
        stock=part.stock,
        supplier_id=supplier_id
    )
    session.add(newPart)
    session.commit()
    session.refresh(newPart)
    return newPart

@app.get('/parts')
def get_all_parts(session: Session=Depends(create_session)):
    parts=session.query(Part).all()
    return parts


#task: try to do search engine optimiztion(even if they type spark plug 'sparkplug' should be displayed)
@app.get('/parts/search')
def get_specific_part_by_name(name:str,session: Session=Depends(create_session)):
    parts=session.query(Part).filter(Part.name==name).all()
    if not parts:
        raise HTTPException(status_code=404, detail="Parts not available")
    return parts

@app.get('/parts/search')
def get_specific_part(car_model:str|None=None,name:str|None=None,session: Session=Depends(create_session)):
    query=session.query(Part)
    if name:
        query1=query.filter(Part.name.ilike(f"%{name}%")).all()
    if car_model:
        query2=query.filter(Part.car_model.ilike(f"%{car_model}%")).all()
    
    parts=query1.extend(query2)
    
    return parts

@app.put('/parts/{supplier_id}/{part_id}')
def update_existing_parts(parts:CreatePart,supplier_id: int,part_id:int, session: Session =Depends(create_session)):
    supplier=session.query(Supplier).filter(Supplier.id==supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404,detail="Not authorised")
    get_part=session.query(Part).filter(Part.id==part_id).first()
    for key,value in dict(parts).items():
        setattr(get_part,key,value)
    setattr(get_part,"supplier_id",supplier_id)
    session.commit()
    return dict(parts)

@app.delete('/parts/{supplier_id}/{part_id}')
def delete_parts(supplier_id: int,part_id:int,session: Session=Depends(create_session)):
    supplier=session.query(Supplier).filter(Supplier.id==supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404,detail="Not authorised")
    get_part=session.query(Part).filter(Part.id==part_id).first()
    session.delete(get_part)
    session.commit()
    return {"message":"part deleted"}