from pydantic import BaseModel
from typing import List

#request body

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str

