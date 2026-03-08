from datetime import timedelta
from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
from database import create_session
from models import User
from sqlalchemy.orm import Session
from hashing import password_hash,DUMMY_HASH
from auth_token import create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import Token
from ..models.user import User

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