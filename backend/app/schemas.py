from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional, Literal

# Employee Schemas
class EmployeeBase(BaseModel):
    employee_id: str = Field(min_length=1, description="Unique employee ID")
    full_name: str = Field(min_length=1, description="Full name of employee")
    email: EmailStr = Field(description="Valid email address")
    department: str = Field(min_length=1, description="Department name")

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    total_present_days: Optional[int] = 0
    
    class Config:
        from_attributes = True

# Attendance Schemas
class AttendanceBase(BaseModel):
    employee_id: str
    date: date
    status: Literal["Present", "Absent"]

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    id: int
    created_at: datetime
    employee_name: Optional[str] = None
    
    class Config:
        from_attributes = True

# Dashboard Schema
class DashboardStats(BaseModel):
    total_employees: int
    total_attendance_records: int
    present_today: int
    absent_today: int