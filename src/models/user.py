from datetime import datetime

from sqlalchemy import func
from sqlalchemy import ForeignKey, LargeBinary, func
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.user_schema import UserSchema


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hash_password: Mapped[bytes] = mapped_column(type_=LargeBinary, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    registration_date: Mapped[datetime] = mapped_column(default=func.now())
    is_active: Mapped[bool] = mapped_column(default=False)

    def to_read_model(self):
        return UserSchema(
            id=self.id,
            username=self.username,
            email=self.email,
            hash_password=self.hash_password,
            role_id=self.role_id,
            registration_date=self.registration_date,
            is_active=self.is_active
        )
    