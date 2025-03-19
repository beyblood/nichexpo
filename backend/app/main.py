from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import users, artists, music, admin 
from app.database import Base, engine  


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Underground Music Discovery")

# Enable CORS (so frontend can access backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust for your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(artists.router, prefix="/api/artists", tags=["Artists"])
app.include_router(music.router, prefix="/api/music", tags=["Music"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/")
def root():
    return {"message": "Welcome to NichExpo API"}

# Run the server with: uvicorn app.main:app --reload
