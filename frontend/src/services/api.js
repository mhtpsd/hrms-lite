import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Employee APIs - Export individual functions
export const getEmployees = () => api.get('/api/employees/');
export const createEmployee = (data) => api.post('/api/employees/', data);
export const deleteEmployee = (id) => api.delete(`/api/employees/${id}`);

// Attendance APIs - Export individual functions
export const getAttendance = (employeeId) => {
  if (employeeId) {
    return api.get(`/api/attendance/employee/${employeeId}`);
  }
  return api.get('/api/attendance/');
};

export const markAttendance = (data) => api.post('/api/attendance/', data);

export const getAttendanceByDate = (date) => 
  api.get('/api/attendance/', { params: { filter_date: date } });

// Dashboard API - Export individual function
export const getDashboardStats = () => api.get('/api/dashboard/stats');

// Export everything as named exports (backward compatibility)
export const employeeAPI = {
  getAll: getEmployees,
  create: createEmployee,
  delete: deleteEmployee,
};

export const attendanceAPI = {
  getAll: getAttendance,
  create: markAttendance,
  getByDate: getAttendanceByDate,
};

export const dashboardAPI = {
  getStats: getDashboardStats,
};