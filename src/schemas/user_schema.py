import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr


class RegisterUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str | bytes


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    hash_password: bytes
    role: str
    registration_date: datetime
    is_active: bool


class UpdateUserDataSchema(BaseModel):
    action: str
    token: str
    password: str | None = None

class JWTUserSchema(BaseModel):
    id: int
    username: str
    role: str

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class TokenInfoSchema(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    
class IssuedJWTTokenSchema(BaseModel):
    id: uuid.UUID
    user_id: int
