from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example route: Get all users
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# Example route: Create a new user
@router.post("/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username, email=user.email, password_hash="hashed_pw")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
