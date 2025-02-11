import asyncio
from app.core.database import SessionLocal
from app.models.models import User, Account, Transaction
from app.routes.hash import hash_password

async def seed_data():
    async with SessionLocal() as db:
        user = User(
            email="user@example.com",
            password=hash_password("user"),
            role="user",
        )

        admin = User(
            email="admin@example.com",
            password=hash_password("admin"),
            role="admin",
        )

        db.add(user)
        db.add(admin)
        await db.commit()
        await db.refresh(user)
        await db.refresh(admin)

        user_account1 = Account(user_id=user.id, balance=500)
        user_account2 = Account(user_id=user.id, balance=1000)
        admin_account = Account(user_id=admin.id, balance=5000)

        db.add(user_account1)
        db.add(user_account2)
        db.add(admin_account)
        await db.commit()

        user_transaction1 = Transaction(
            user_id=user.id,
            account_id=user_account1.id,
            amount=500,
        )
        user_transaction2 = Transaction(
            user_id=user.id,
            account_id=user_account2.id,
            amount=700,
        )
        user_transaction3 = Transaction(
            user_id=user.id,
            account_id=user_account2.id,
            amount=300,
        )
        admin_transaction = Transaction(
            user_id=admin.id,
            account_id=admin_account.id,
            amount=5000,
        )

        db.add(user_transaction1)
        db.add(user_transaction2)
        db.add(user_transaction3)
        db.add(admin_transaction)
        await db.commit()

        print("✅ Данные успешно добавлены в БД!")

if __name__ == "__main__":
    asyncio.run(seed_data())
