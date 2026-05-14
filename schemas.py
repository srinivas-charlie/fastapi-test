from pydantic import BaseModel, EmailStr
from typing import Optional


# ======================================
# USER CREATE
# ======================================
class UserCreate(BaseModel):

    name: str

    email: EmailStr

    password: str


# ======================================
# USER RESPONSE
# ======================================
class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    role: str

    class Config:
        from_attributes = True


# ======================================
# ROLE UPDATE
# ======================================
class RoleUpdate(BaseModel):

    role: str


# ======================================
# PROFILE UPDATE
# ======================================
class ProfileUpdate(BaseModel):

    name: Optional[str] = None

    email: Optional[EmailStr] = None