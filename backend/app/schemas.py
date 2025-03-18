from pydantic import BaseModel
from typing import Optional

# User Schema
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# Artist Schema
class ArtistBase(BaseModel):
    user_id: int
    country: str
    city: str
    genre: str
    social_links: Optional[str] = None

class ArtistCreate(ArtistBase):
    pass

class ArtistResponse(ArtistBase):
    id: int

    class Config:
        from_attributes = True

# ✅ Add the missing MusicCreate schema
class MusicBase(BaseModel):
    artist_id: int
    title: str
    genre: str
    file_url: str  # URL of the uploaded music file

class MusicCreate(MusicBase):
    pass

class MusicResponse(MusicBase):
    id: int

    class Config:
        from_attributes = True
