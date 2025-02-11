import json
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException, Depends, Request

from app.schemas.schemas import AuthSchema
from app.models.models import User, Account, Payment
from app.core.database import get_db

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

    access_token = create_access_token(data=data)
    refresh_token = create_refresh_token(data=data)

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

    access_token = create_access_token(data=data)
    refresh_token = create_refresh_token(data=data)

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
        access_token = create_access_token(data=user_data)
        return {'access_token': access_token, 'token_type': 'bearer'}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

