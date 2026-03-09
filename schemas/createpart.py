from pydantic import BaseModel

class CreatePart(BaseModel):
    name: str
    description:str
    price:float
    car_model:str
    stock: int