from datetime import datetime, timezone
from sqlalchemy import ForeignKey, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hash_password: Mapped[bytes] = mapped_column(type_=LargeBinary, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(default=False)
