from pydantic import BaseModel, EmailStr
from uuid import UUID


class AuthSchema(BaseModel):
    email: EmailStr
    password: str


class TransactionSchema(BaseModel):
    transaction_id: UUID
    account_id: UUID
    user_id: UUID
    amount: int
    signature: str
