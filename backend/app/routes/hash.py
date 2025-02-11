import hashlib
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def generate_signature(transaction_id: int, user_id: int, account_id: int, amount: int):
    data_string = f"{account_id}{amount}{transaction_id}{user_id}{settings.SECRET_KEY}"
    return hashlib.sha256(data_string.encode()).hexdigest()

