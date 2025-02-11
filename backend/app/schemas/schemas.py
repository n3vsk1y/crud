from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


class AuthSchema(BaseModel):
    email: EmailStr
    password: str


class TransactionSchema(BaseModel):
    transaction_id: UUID
    account_id: UUID
    user_id: UUID
    amount: int
    signature: str


class UserSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = None

