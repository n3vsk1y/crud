from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import Base, engine

from fastapi import Depends
from app.core.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.future import select


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     yield


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.get("/")
def read_root():
    return {"App": "Started"}


@app.get("/check")
async def check_bd(db: Session = Depends(get_db)):
    try:
        result = await db.execute(select(1))
        return {"status": "success", "message": "Database success connection"}
    except Exception as e:
        return {"status": "error", "message": f"Database connection failed: {str(e)}"}
