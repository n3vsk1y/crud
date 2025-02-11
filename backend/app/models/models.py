import uuid
from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, default="user")
    refresh_token: Mapped[str] = mapped_column(String, nullable=True)

    accounts = relationship('Account', back_populates='user')


class Account(Base):
    __tablename__ = 'accounts'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    balance: Mapped[float] = mapped_column(Float, default=0.0)

    user = relationship('User', back_populates='accounts')
    transactions = relationship('Transaction', back_populates='account')


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('accounts.id'), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    time: Mapped[DateTime] = mapped_column(DateTime, default=func.now())

    account = relationship('Account', back_populates='transactions')
