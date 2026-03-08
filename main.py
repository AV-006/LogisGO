from datetime import timedelta
from typing import Optional
from fastapi import FastAPI,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .models.user import User,Base
from .models.supplier import Supplier
from database import engine,create_session
from schemas import UserCreate,Token,CreatePart
from hashing import password_hash,DUMMY_HASH
from auth_token import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from .routers import authentication,parts
app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(parts.router)


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




