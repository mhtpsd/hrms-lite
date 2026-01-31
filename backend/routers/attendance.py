from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import get_db

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Attendance)
def mark_attendance(attendance: schemas.AttendanceCreate, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db, employee_id=attendance.employee_id)
    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return crud.create_attendance(db=db, attendance=attendance)

@router.get("/{employee_id}", response_model=List[schemas.Attendance])
def read_attendance(employee_id: int, db: Session = Depends(get_db)):
    attendance_records = crud.get_attendance(db, employee_id=employee_id)
    return attendance_records
