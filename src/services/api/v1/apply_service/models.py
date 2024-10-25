from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime
from datetime import datetime
from src.config.apply_database import ApplyBASE
from sqlalchemy.dialects.postgresql import UUID
import uuid


class ApplyModel(ApplyBASE):
    __tablename__ = "applys"

    id: Mapped[int] = mapped_column(Integer, index=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    cv_id: Mapped[int] = mapped_column(Integer)
    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    latter: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=False)
