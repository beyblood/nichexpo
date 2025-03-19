from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import SessionLocal
from .schemas import UserCreate, UserLogin, Token
from .models import User
from .services.auth_service import hash_password, verify_password, create_access_token
from datetime import timedelta
import os

auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@auth_router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return a JWT token."""
    existing_user = db.query(User).filter_by(username=user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user_data.password)
    new_user = User(username=user_data.username, password_hash=hashed_password, role=user_data.role)  # ✅ Fixed password_hash

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({"sub": new_user.username, "role": new_user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = db.query(User).filter_by(username=user_data.username).first()
    if not user or not verify_password(user_data.password, user.password_hash):  # ✅ Fixed password_hash
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # ✅ Use .env instead of hardcoding
    access_token = create_access_token({"sub": user.username, "role": user.role}, timedelta(minutes=expire_minutes))

    return {"access_token": access_token, "token_type": "bearer"}
