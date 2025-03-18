from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_artist = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    artist_profile = relationship("Artist", back_populates="user")

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    country = Column(String)
    city = Column(String)
    genre = Column(String)
    social_links = Column(String)

    user = relationship("User", back_populates="artist_profile")
