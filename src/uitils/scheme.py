from pydantic import BaseModel
from typing import Optional


class SUser(BaseModel):

    id: int
    username: str
    picture_url: Optional[str] = None
    email: str

    age: int
    name: str
    surname: str
    role: str
    company_name: Optional[str] = None
    token: Optional[str] = None
    
