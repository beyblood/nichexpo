from fastapi import FastAPI
from .routes import artists, users, auth
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NichExpo API")

# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(artists.router, prefix="/artists", tags=["Artists"])

@app.get("/")
def read_root():
    return {"message": "Welcome to NichExpo API"}
