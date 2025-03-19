from pydantic import BaseModel, EmailStr
from typing import Optional

# ==========================
# ✅ User Schemas
# ==========================
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str  # "user", "artist", or "admin"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    username: str
    role: str

# ==========================
# ✅ Artist Schemas
# ==========================
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

# ==========================
# ✅ Music Schemas
# ==========================
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
