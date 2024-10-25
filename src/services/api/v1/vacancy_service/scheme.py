from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from src.uitils.scheme import SUser
from typing import Optional
import uuid


class WorkCategory(Enum):

    SOFTWARE_ENGINE = "Разработчик"
    COOCKER = "Повар"
    POLICE = "Полицейский"
    FIREMAN = "Пожарный"
    ATTORNEY = "Адвокат"
    TEACHER = "Учитель"
    DOCTOR = "Доктор"
    OTHER = "Другое"


class VacancyResponse(BaseModel):

    id: uuid.UUID
    work_category: str
    date_pub: datetime
    vacancy_title: str

    user: Optional[SUser] = None
    location: str
    description: str
    conditions: str

    price: int
    key_skils: str
    experience: int
    is_exist: bool
    user_id: Optional[int] = None
