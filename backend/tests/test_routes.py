import hashlib
import pytest
import os
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from main import app
from app.core.database import get_async_session, Base

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture
async def session():
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
async def client(session):
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac

app.dependency_overrides[get_async_session] = lambda: session

def generate_signature(data):
    sorted_values = f"{data['account_id']}{data['amount']}{data['transaction_id']}{data['user_id']}{SECRET_KEY}"
    return hashlib.sha256(sorted_values.encode()).hexdigest()

@pytest.mark.asyncio
async def test_webhook_payment(client, session):
    # Данные вебхука
    webhook_data = {
        "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
        "user_id": 1,
        "account_id": 1,
        "amount": 100
    }
    
    webhook_data["signature"] = generate_signature(webhook_data)
    
    response = await client.post("/webhook/payment", json=webhook_data)
о
    assert response.status_code == 200
    assert response.json() == {"message": "Payment processed successfully"}
