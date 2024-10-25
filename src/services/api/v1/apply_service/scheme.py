from pydantic import BaseModel
from typing import Optional, List
from src.services.api.v1.vacancy_service.scheme import VacancyResponse, SUser
from src.services.api.v1.cv_service.scheme import CvResponse
from datetime import datetime


class ApplyResponse(BaseModel):
    id: int
    cv_response: Optional[CvResponse] = None
    vacancy: Optional[VacancyResponse] = None
    user: Optional[SUser] = None
    created_at: datetime
    status: str
    user_id: Optional[int] = None
