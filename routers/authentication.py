from datetime import timedelta
from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from database import create_session
from sqlalchemy.orm import Session
from hashing import password_hash,DUMMY_HASH
from auth_token import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from schemas.token import Token
from models.user import User
from models.supplier import Supplier
from schemas.createuser import UserCreate

router=APIRouter(tags=["Authentication"])
#login route


@router.post('/auth/login')
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

@router.post('/auth/signup')
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