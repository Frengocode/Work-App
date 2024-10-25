from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from src.config.cv_database import CVServiceDB
from datetime import datetime


class CvModel(CVServiceDB):
    __tablename__ = "user_cv"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    specialization: Mapped[str] = mapped_column(String, nullable=False)
    post: Mapped[str] = mapped_column(String, nullable=False)  # должность

    amusement: Mapped[str] = mapped_column(String, nullable=False)
    schedule: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[int] = mapped_column(Integer, nullable=False)

    experience: Mapped[int] = mapped_column(Integer, nullable=False)
    experience_about: Mapped[str] = mapped_column(String, nullable=False)
    skils: Mapped[str] = mapped_column(String, nullable=False)

    about_of_me: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    user_id: Mapped[int] = mapped_column(Integer, nullable=True)
