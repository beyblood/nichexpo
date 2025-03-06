from fastapi import FastAPI
from routes import users, artists, music

app = FastAPI()

# Register API routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(artists.router, prefix="/artists", tags=["Artists"])
app.include_router(music.router, prefix="/music", tags=["Music"])

@app.get("/")
def home():
    return {"message": "Welcome to NichExpo"}
