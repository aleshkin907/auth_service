from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.user_schema import IssuedJWTTokenSchema


class IssuedJWTToken(Base):
    __tablename__ = "tokens"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    def to_read_model(self):
        return IssuedJWTTokenSchema(
            jti=self.jti,
            user_id=self.user_id
        )
