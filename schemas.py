from pydantic import BaseModel
from typing import List

#request body

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str
    location: str

class CreatePart(BaseModel):
    name: str
    description:str
    price:float
    car_model:str
    stock: int

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    email: str | None=None