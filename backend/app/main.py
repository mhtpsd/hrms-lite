from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import employees, attendance

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Attendance API")

# CORS middleware
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
def read_root():
    return {"message": "Employee Attendance API is running"}