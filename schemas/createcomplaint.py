from pydantic import BaseModel
from typing import List

class PostComplaint(BaseModel):
    complaint: str
    