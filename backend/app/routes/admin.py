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

# Example route: Get all artists awaiting approval
@router.get("/pending_artists")
def get_pending_artists(db: Session = Depends(get_db)):
    artists = db.query(models.Artist).filter(models.Artist.approved == False).all()  # Assuming 'approved' is a column in your Artist model
    return artists

# Example route: Approve an artist
@router.post("/approve_artist/{artist_id}")
def approve_artist(artist_id: int, db: Session = Depends(get_db)):
    artist = db.query(models.Artist).filter(models.Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")
    
    artist.approved = True
    db.commit()
    db.refresh(artist)
    return {"message": f"Artist {artist_id} approved."}
