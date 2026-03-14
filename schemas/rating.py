from pydantic import BaseModel,Field

class CreateRating(BaseModel):
    rating: float =Field(...,ge=1,le=5)