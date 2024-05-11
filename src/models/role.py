from sqlalchemy.orm import Mapped, mapped_column

from db.db import Base
from schemas.role_schema import RoleSchema


class Role(Base):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    def to_read_model(self):
        return RoleSchema(
            id=self.id,
            name=self.name
        )