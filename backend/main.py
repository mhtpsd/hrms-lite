from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import employees, attendance

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="HRMS Lite API")

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "*" # For ease of development/testing, update for prod
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(attendance.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to HRMS Lite API"}
