from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from ..core.mongo import next_sequence, users_collection
from ..core.security import create_access_token, get_password_hash, verify_password
from ..schemas.auth import LoginRequest, RegisterRequest, Token
from ..schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register(payload: RegisterRequest):
    existing = await users_collection.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = await next_sequence("users")
    user_doc = {
        "_id": user_id,
        "email": payload.email,
        "hashed_password": get_password_hash(payload.password),
        "is_active": True,
        "is_admin": payload.is_admin,
        "created_at": datetime.utcnow(),
    }
    await users_collection.insert_one(user_doc)
    return {"id": user_id, "email": payload.email, "is_admin": payload.is_admin}


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest):
    user = await users_collection.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user["email"])
    return Token(access_token=token)

