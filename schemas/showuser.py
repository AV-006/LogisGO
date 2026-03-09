from pydantic import BaseModel

class ShowUser(BaseModel):
    name: str
    role: str
    
    class Config:
        orm_mode=True