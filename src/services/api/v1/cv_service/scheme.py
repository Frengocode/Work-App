from pydantic import BaseModel
from typing import Optional
from src.uitils.scheme import SUser
from datetime import datetime


class CvResponse(BaseModel):

    id: Optional[int] = None
    user: Optional[SUser] = None
    specialization: Optional[str] = None
    amusement: Optional[str] = None
    post: Optional[str] = None
    skils: Optional[str] = None
    schedule: Optional[str] = None
    experience: Optional[int] = None
    experience_about: Optional[str] = None
    about_of_me: Optional[str] = None
    create_at: Optional[datetime] = None



class CVUpdateRequest(BaseModel):
    specializitaion: str
    amusement: str
    schedule: str
    phone_number: int
    exprience: int
    exprience_about: str
    skils: str
    about_of_me: str