from uuid import UUID
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Depends, Request

from app.schemas.schemas import AuthSchema, TransactionSchema, UserSchema
from app.models.models import User, Account, Transaction
from app.core.database import get_db
from app.core.orm import get_user

from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from app.routes.hash import hash_password, verify_password, generate_signature

from app.routes.jwt_tokens import create_access_token, create_refresh_token, verify_token
from fastapi.responses import JSONResponse


router = APIRouter(prefix='/api', tags=['API'])


@router.post('/login')
async def login(data: AuthSchema, db: Session = Depends(get_db)):
    query = select(User).where(User.email == data.email)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=404, detail='Invalid email or password')

    data = {
        'user_id': str(user.id),
        'email': user.email,
        'role': 'user',
    }

    access_token = await create_access_token(data=data)
    refresh_token = await create_refresh_token(data=data)
    user.refresh_token = refresh_token
    await db.commit()

    response = JSONResponse(content={
        'access_token': access_token,
        'token_type': 'bearer',
    })

    expires = datetime.now(timezone.utc) + timedelta(days=30)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="None",
        max_age=30 * 24 * 60 * 60,  # кука живет 30 дней
        expires=expires,
        path="/",
    )

    return response


@router.post('/signup')
async def signup(data: AuthSchema, db: Session = Depends(get_db)):
    query = select(User).where(User.email == data.email)
    result = await db.execute(query)
    user = result.scalars().first()
    if user:
        raise HTTPException(status_code=409, detail='User already exists')

    hashed_password = hash_password(data.password)
    new_user = User(email=data.email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    data = {
        'user_id': str(new_user.id),
        'email': new_user.email,
        'role': 'user',
    }

    access_token = await create_access_token(data=data)
    refresh_token = await create_refresh_token(data=data)

    new_user.refresh_token = refresh_token
    await db.commit()

    response = JSONResponse(content={
        'access_token': access_token,
        'token_type': 'bearer',
    })

    expires = datetime.now(timezone.utc) + timedelta(days=30)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="None",
        max_age=30 * 24 * 60 * 60,  # кука живет 30 дней
        expires=expires,
        path="/",
    )

    return response


@router.post('/refresh')
async def refresh_token(request: Request):
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        raise HTTPException(status_code=401, detail='Refresh token not found')
    try:
        payload = verify_token(refresh_token)
        user_data = payload['data']
        access_token = await create_access_token(data=user_data)
        return {'access_token': access_token, 'token_type': 'bearer'}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


{
    "transaction_id": "5eae174f-7cd0-472c-bd36-35660f00132b",
    "user_id": "6dcf34de-470f-4399-a61d-deda8e96e0cd",
    "account_id": "6dcf34de-470f-4399-a61d-deda8e96e0cd",
    "amount": 100,
    "signature": "0bb95902a7fc463da70fd91c098ed9efd993c11b6bb7a0cf8b2947d590ca1afd"
}
{
    "transaction_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "user_id": "6dcf34de-470f-4399-a61d-deda8e96e0cd",
    "account_id": "6dcf34de-470f-4399-a61d-deda8e96e0cd",
    "amount": 150,
    "signature": "707b35be0ea869817b11c22bcdb6b5681d36d922890c5587e13787636dd7138f"
}
{
    "transaction_id": "a2d968ea-92f0-4c0d-9185-6b661044614d",
    "user_id": "6dcf34de-470f-4399-a61d-deda8e96e0cd",
    "account_id": "30def338-25c5-4c0b-8b4e-aee74936e3ae",
    "amount": 150,
    "signature": "d1199ab5952a122df480c705682f9868a1c70c5e4c67ee8bea0a66dd8b1ef4b7"
}


@router.post("/webhook")
async def process_transaction(data: TransactionSchema, db: AsyncSession = Depends(get_db)):
    expected_signature = await generate_signature(data.transaction_id, data.user_id, data.account_id, data.amount)
    if data.signature != expected_signature:
        raise HTTPException(status_code=400, detail="Invalid signature")

    query = select(Transaction).where(Transaction.id == data.transaction_id)
    existing_transaction = await db.execute(query)
    if existing_transaction.scalars().first():
        raise HTTPException(
            status_code=400, detail="Transaction already processed")

    query = select(Account).where(Account.id == data.account_id)
    existing_account = await db.execute(query)
    account = existing_account.scalars().first()

    if not account:
        new_account = Account(id=data.account_id,
                              user_id=data.user_id, balance=data.amount)
        db.add(new_account)
        await db.commit()
        await db.refresh(new_account)

    new_transaction = Transaction(
        id=data.transaction_id,
        account_id=data.account_id,
        user_id=data.user_id,
        amount=data.amount,
    )
    db.add(new_transaction)
    await db.commit()

    if account:
        account.balance += data.amount
    await db.commit()

    return {"message": "Trasnsaction processed"}


@router.post("/set_name")
async def set_name(full_name: str, db: Session = Depends(get_db), current_user=Depends(get_user)):
    try:
        current_user.full_name = full_name
        await db.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set name: {e}")


@router.get("/get_user_info")
async def get_info(current_user=Depends(get_user)):
    try:
        answer = {
            'id': current_user.id,
            'email': current_user.email,
            'full_name': current_user.full_name,
        }
        return answer
    
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get user info: {e}")


@router.get("/get_user_accounts")
async def get_user_accounts(db: Session = Depends(get_db), current_user=Depends(get_user)):
    try:
        query = select(Account).where(Account.user_id == current_user.id)
        result = await db.execute(query)
        accounts = result.fetchall()
        accounts_dict = [{"account_id": account.id, "balance": account.balance} for account, in accounts]

        return accounts_dict

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get accounts: {e}")


@router.get("/get_user_transactions")
async def get_user_transactions(db: Session = Depends(get_db), current_user=Depends(get_user)):
    try:
        query = select(Transaction).where(Transaction.user_id == current_user.id)
        result = await db.execute(query)
        
        transactions = result.fetchall()
        
        transactions_dict = [{"transaction_id": transaction.id, "amount": transaction.amount, "time": transaction.time} for transaction, in transactions]
        
        return transactions_dict
    
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get transactions: {e}")


@router.get("/get_all_accounts")
async def get_all_accounts(db: Session = Depends(get_db), current_user=Depends(get_user)):
    try:
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Permission denied")
        
        query = select(Account)
        result = await db.execute(query)
        accounts = result.fetchall()

        accounts_dict = {}

        for account, in accounts:
            if account.user_id not in accounts_dict:
                accounts_dict[account.user_id] = []

            accounts_dict[account.user_id].append({"account_id": account.id, "balance": account.balance})

        return accounts_dict

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get accounts: {e}")


@router.post("/create_user")
async def create_user(data: UserSchema, db: Session = Depends(get_db), current_user=Depends(get_user)):
    try:
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Permission denied")

        new_user = User(
            email=data.email,
            password=hash_password(data.password),
            full_name=data.full_name,
            role=data.role,
        )

        db.add(new_user)
        db.commit()

        return {"message": "User created successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {e}")
    

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: str, db: Session = Depends(get_db), current_user=Depends(get_user)):
    try:
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Permission denied")
        
        query = select(User).where(User.id == user_id)
        result = db.execute(query)
        user = result.scalars().first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()

        return {"message": "User deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {e}")


@router.put("/update_user/{user_id}")
async def update_user(user_id: str, data: UserSchema, db: Session = Depends(get_db), current_user=Depends(get_user)):
    try:
        if current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Permission denied")
        
        query = select(User).where(User.id == user_id)
        result = db.execute(query)
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if data.email:
            user.email = data.email
        if data.password:
            user.password = hash_password(data.password)
        if data.full_name is not None:
            user.full_name = data.full_name
        if data.role is not None:
            user.role = data.role

        db.commit()

        return {"message": "User updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {e}")
