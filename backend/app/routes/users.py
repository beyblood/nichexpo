from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, database
from ..services.auth_service import get_current_user, hash_password

router = APIRouter(prefix="/api/users", tags=["Users"])

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all users
@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

# Create a new user with proper password hashing
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_pw = hash_password(user.password)
    
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_pw,
        role=user.role  # ✅ Include role when saving to the database
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# Get the current user's profile
@router.get("/profile", response_model=schemas.UserProfile)
def get_profile(user: dict = Depends(get_current_user)):
    """Return user profile based on JWT token."""
    return schemas.UserProfile(username=user["sub"], role=user["role"])
