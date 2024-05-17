from typing import Literal
from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    email_type: Literal["verification", "reset"]
    username: str
    email: EmailStr
    token: str
    