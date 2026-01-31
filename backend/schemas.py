from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# Employee Schemas
class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    department: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    created_at: date

    class Config:
        from_attributes = True

# Attendance Schemas
class AttendanceBase(BaseModel):
    date: date
    status: str

class AttendanceCreate(AttendanceBase):
    employee_id: int # Internal DB ID

class Attendance(AttendanceBase):
    id: int
    employee_id: int

    class Config:
        from_attributes = True
