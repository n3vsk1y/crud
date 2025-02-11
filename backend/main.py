from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import api
from app.core.database import Base, engine

from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import inspect, text


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield


app = FastAPI()

app.include_router(api.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.get("/")
def read_root():
    return {"App": "Started"}


@app.get("/check_bd")
async def check_bd(db: Session = Depends(get_db)):
    try:
        async with db.begin():
            result = await db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
            tables = [row[0] for row in result.fetchall()]
            return {"status": "success", "message": f"Tables: {tables}"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}
