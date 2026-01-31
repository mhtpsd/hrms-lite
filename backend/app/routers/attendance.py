from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/api/attendance", tags=["attendance"])

@router.post("/", response_model=schemas.AttendanceResponse, status_code=201)
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    """Mark attendance for an employee"""
    return crud.create_attendance(db, attendance)

@router.get("/", response_model=List[schemas.AttendanceResponse])
def get_all_attendance(
    filter_date: Optional[date] = Query(None, description="Filter by date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get all attendance records with optional date filter"""
    return crud.get_all_attendance(db, filter_date)

@router.get("/employee/{employee_id}", response_model=List[schemas.AttendanceResponse])
def get_employee_attendance(employee_id: str, db: Session = Depends(get_db)):
    """Get attendance records for a specific employee"""
    return crud.get_employee_attendance(db, employee_id)