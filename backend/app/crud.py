from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from . import models, schemas
from fastapi import HTTPException, status

# Employee CRUD
def get_employees(db: Session):
    employees = db.query(models.Employee).all()
    
    # Add total present days for each employee
    result = []
    for emp in employees:
        emp_dict = {
            "id": emp.id,
            "employee_id": emp.employee_id,
            "full_name": emp.full_name,
            "email": emp.email,
            "department": emp.department,
            "created_at": emp.created_at,
            "total_present_days": db.query(models.Attendance).filter(
                models.Attendance.employee_id == emp.employee_id,
                models.Attendance.status == models.AttendanceStatus.PRESENT
            ).count()
        }
        result.append(emp_dict)
    
    return result

def get_employee(db: Session, employee_id: str):
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    # Check for duplicate employee_id
    existing_emp_id = db.query(models.Employee).filter(models.Employee.employee_id == employee.employee_id).first()
    if existing_emp_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee ID already exists")
    
    # Check for duplicate email
    existing_email = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    db_employee = models.Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, employee_id: str):
    employee = get_employee(db, employee_id)
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

# Attendance CRUD
def create_attendance(db: Session, attendance: schemas.AttendanceCreate):
    # Check if employee exists
    employee = db.query(models.Employee).filter(models.Employee.employee_id == attendance.employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    # Check for duplicate attendance on same date
    existing = db.query(models.Attendance).filter(
        models.Attendance.employee_id == attendance.employee_id,
        models.Attendance.date == attendance.date
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Attendance already marked for this employee on {attendance.date}"
        )
    
    db_attendance = models.Attendance(**attendance.model_dump())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

def get_all_attendance(db: Session, filter_date: date = None):
    query = db.query(models.Attendance)
    
    if filter_date:
        query = query.filter(models.Attendance.date == filter_date)
    
    records = query.order_by(models.Attendance.date.desc()).all()
    
    # Add employee name to each record
    result = []
    for record in records:
        employee = db.query(models.Employee).filter(models.Employee.employee_id == record.employee_id).first()
        record_dict = {
            "id": record.id,
            "employee_id": record.employee_id,
            "date": record.date,
            "status": record.status,
            "created_at": record.created_at,
            "employee_name": employee.full_name if employee else "Unknown"
        }
        result.append(record_dict)
    
    return result

def get_employee_attendance(db: Session, employee_id: str):
    # Check if employee exists
    employee = db.query(models.Employee).filter(models.Employee.employee_id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    
    records = db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id
    ).order_by(models.Attendance.date.desc()).all()
    
    # Add employee name
    result = []
    for record in records:
        record_dict = {
            "id": record.id,
            "employee_id": record.employee_id,
            "date": record.date,
            "status": record.status,
            "created_at": record.created_at,
            "employee_name": employee.full_name
        }
        result.append(record_dict)
    
    return result

def get_dashboard_stats(db: Session):
    total_employees = db.query(models.Employee).count()
    total_attendance = db.query(models.Attendance).count()
    
    today = date.today()
    present_today = db.query(models.Attendance).filter(
        models.Attendance.date == today,
        models.Attendance.status == models.AttendanceStatus.PRESENT
    ).count()
    
    absent_today = db.query(models.Attendance).filter(
        models.Attendance.date == today,
        models.Attendance.status == models.AttendanceStatus.ABSENT
    ).count()
    
    return {
        "total_employees": total_employees,
        "total_attendance_records": total_attendance,
        "present_today": present_today,
        "absent_today": absent_today
    }