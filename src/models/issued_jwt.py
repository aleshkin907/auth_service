from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base


class IssuedJWTToken(Base):
    __tablename__ = "tokens"

    jti: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(default=False)
