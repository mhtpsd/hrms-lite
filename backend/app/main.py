from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import employees, attendance
from . import crud
from .database import SessionLocal
import os
from dotenv import load_dotenv

load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HRMS Lite API",
    description="Lightweight Human Resource Management System",
    version="1.0.0"
)

# CORS Configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(employees.router)
app.include_router(attendance.router)

@app.get("/")
def root():
    return {
        "message": "HRMS Lite API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    db = SessionLocal()
    try:
        return crud.get_dashboard_stats(db)
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {"status": "healthy"}