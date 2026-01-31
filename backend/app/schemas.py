from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date, datetime
from typing import Optional
from enum import Enum

# Attendance Status Enum
class AttendanceStatusEnum(str, Enum):
    PRESENT = "Present"
    ABSENT = "Absent"

# Employee Schemas
class EmployeeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    employee_id: str = Field(..., min_length=1, description="Unique employee ID")
    full_name: str = Field(..., min_length=1, description="Full name of employee")
    email: EmailStr = Field(..., description="Valid email address")
    department: str = Field(..., min_length=1, description="Department name")

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime
    total_present_days: Optional[int] = 0

# Attendance Schemas
class AttendanceBase(BaseModel):
    model_config = ConfigDict(use_enum_values=False)
    
    employee_id: str = Field(..., description="Employee ID")
    date: date = Field(..., description="Attendance date")
    status: AttendanceStatusEnum = Field(..., description="Present or Absent")

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceResponse(AttendanceBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=False)
    
    id: int
    created_at: datetime
    employee_name: Optional[str] = None

# Dashboard Schema
class DashboardStats(BaseModel):
    total_employees: int
    total_attendance_records: int
    present_today: int
    absent_today: int