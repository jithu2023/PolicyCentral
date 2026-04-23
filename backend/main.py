# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import admin, recommendation, chat
from database import init_db

app = FastAPI()

# Initialize database
init_db()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin.router)
app.include_router(recommendation.router)
app.include_router(chat.router)

@app.get("/")
def home():
    return {"message": "Backend stable 🚀", "status": "ready"}