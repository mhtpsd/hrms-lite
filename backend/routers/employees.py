from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud, models, schemas
from database import get_db

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_emp = crud.get_employee_by_email(db, email=employee.email)
    if db_emp:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_emp_id = crud.get_employee_by_emp_id(db, emp_id=employee.employee_id)
    if db_emp_id:
        raise HTTPException(status_code=400, detail="Employee ID already registered")
    return crud.create_employee(db=db, employee=employee)

@router.get("/", response_model=List[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = crud.get_employees(db, skip=skip, limit=limit)
    return employees

@router.delete("/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    success = crud.delete_employee(db=db, employee_id=employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}
