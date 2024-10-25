from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from src.config.database import VacancyServiceDB
import uuid


class VacancyModel(VacancyServiceDB):
    __tablename__ = "vacancys"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    vacancy_title: Mapped[str] = mapped_column(String, nullable=False)
    work_category: Mapped[str] = mapped_column(String, nullable=False)

    experience: Mapped[int] = mapped_column(Integer, nullable=False)
    key_skils: Mapped[str] = mapped_column(String, nullable=False)
    is_exist: Mapped[bool] = mapped_column(Boolean, default=True)

    location: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    conditions: Mapped[str] = mapped_column(String, nullable=False)

    price: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    date_of_pub: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
