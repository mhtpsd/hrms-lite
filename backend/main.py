from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import employees, attendance
from app import crud
from app.database import SessionLocal

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HRMS Lite API",
    description="Lightweight Human Resource Management System",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/dashboard/stats")
def get_dashboard_stats():
    """Get dashboard statistics"""
    db = SessionLocal()
    try:
        return crud.get_dashboard_stats(db)
    finally:
        db.close()