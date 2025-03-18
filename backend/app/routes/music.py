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

# Example route: Get all music tracks
@router.get("/")
def get_music(db: Session = Depends(get_db)):
    music_tracks = db.query(models.Music).all()
    return music_tracks

# Example route: Upload a new music fragment
@router.post("/")
def upload_music(music: schemas.MusicCreate, db: Session = Depends(get_db)):
    db_music = models.Music(
        artist_id=music.artist_id,
        title=music.title,
        genre=music.genre,
        file_url=music.file_url,  # This should be handled by a file upload service
    )
    db.add(db_music)
    db.commit()
    db.refresh(db_music)
    return db_music
