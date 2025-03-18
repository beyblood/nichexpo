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

# Example route: Get all artists
@router.get("/")
def get_artists(db: Session = Depends(get_db)):
    artists = db.query(models.Artist).all()
    return artists

# Example route: Create a new artist profile
@router.post("/")
def create_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    db_artist = models.Artist(
        user_id=1,  # Replace this with actual logic to get user ID
        country=artist.country,
        city=artist.city,
        genre=artist.genre,
        social_links=artist.social_links,
    )
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist
