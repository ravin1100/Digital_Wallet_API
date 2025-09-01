from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    phone_number: str = Field(pattern=r"^[6-9]\d{9}$")
    password: str = Field(min_length=8)
    balance: float = Field(default=0.00, ge=0)

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    balance: Optional[float] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str
    password: str
    balance: float

    class Config:
        from_attributes = True
