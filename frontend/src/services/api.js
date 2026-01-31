import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Employee APIs
export const employeeAPI = {
  getAll: () => api.get('/api/employees/'),
  create: (data) => api.post('/api/employees/', data),
  delete: (id) => api.delete(`/api/employees/${id}`),
};

// Attendance APIs
export const attendanceAPI = {
  getAll: (date) => api.get('/api/attendance/', { params: { filter_date: date } }),
  create: (data) => api.post('/api/attendance/', data),
};

// Dashboard API
export const dashboardAPI = {
  getStats: () => api.get('/api/dashboard/stats'),
};