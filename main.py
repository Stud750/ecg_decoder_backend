from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
<<<<<<< HEAD
from authx import AuthX, AuthXConfig, RequestToken, TokenPayload
=======
from authx import AuthX, AuthXConfig
>>>>>>> c1407f225bc6847926689acf2fdfa35d1b263f6a
from sqlalchemy import select
from dotenv import dotenv_values

from postgres_db import get_session
from models import User, Patient
from schemas import UserLoginSchema, PatientHistoryItem, UserProfileSchema


app = FastAPI()

tokens_and_keys = dotenv_values(".env")

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

config = AuthXConfig()
config.JWT_SECRET_KEY = tokens_and_keys['SECRET_KEY']
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


@app.post("/login")
async def login(
    creds: UserLoginSchema,
    response: Response,
    session=Depends(get_session)
):
    query = select(User).where(User.email == creds.email)
    result = await session.execute(query)
    user = result.scalar()
    if not user:
        raise HTTPException(status_code=401, detail="incorrect username or password")
    if creds.password != user.password:
        raise HTTPException(status_code=401, detail="incorrect username or password")
    token = security.create_access_token(uid=str(user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token, max_age=28800)

    return {"access_token": token}


@app.get("/check-auth")
async def check_auth(user_id: str = Depends(security.access_token_required)):
    return {"status": "ok", "user_id": user_id}

@app.get("/history", response_model=list[PatientHistoryItem])
async def history(
    q: str | None = None,
    token_payload: TokenPayload = Depends(security.access_token_required),
    session=Depends(get_session)
):
    
    doctor_id = int(token_payload.sub)

    query = select(Patient).where(Patient.doctor_id == doctor_id)

    if q:
        q = f"%{q.lower()}%"
        query = query.where(
            (Patient.last_name.ilike(q)) |
            (Patient.first_name.ilike(q)) |
            (Patient.middle_name.ilike(q)) |
            (Patient.file_name.ilike(q)) 
        )

    result = await session.execute(query)
    rows = result.scalars().all()

    return rows



@app.get("/profile", response_model=UserProfileSchema)
async def get_profile(
    token_payload: TokenPayload = Depends(security.access_token_required),
    session=Depends(get_session)
):
    
    user_id = int(token_payload.sub)

    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8000)

