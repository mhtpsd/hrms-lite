# HRMS Lite - Backend API

FastAPI-based backend for the Human Resource Management System.

## Requirements

- Python 3.10+ (tested on Python 3.14.2)
- pip

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or for production (PostgreSQL support):
```bash
pip install -r requirements-prod.txt
```

## Running the Server

### Development Mode (with auto-reload):
```bash
python -m uvicorn app.main:app --reload --port 8000
```

### Production Mode:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Environment Variables

Create a `.env` file in the backend directory with:

```env
DATABASE_URL=sqlite:///./hrms.db
CORS_ORIGINS=http://localhost:5173
```

For PostgreSQL:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

## API Endpoints

### Employees
- `GET /api/employees/` - List all employees
- `POST /api/employees/` - Create new employee
- `GET /api/employees/{employee_id}` - Get employee by ID
- `DELETE /api/employees/{employee_id}` - Delete employee

### Attendance
- `GET /api/attendance/` - List all attendance records
- `POST /api/attendance/` - Mark attendance
- `GET /api/attendance/employee/{employee_id}` - Get employee attendance history

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics

## Database

The application uses SQLite by default. The database file (`hrms.db`) will be created automatically on first run.