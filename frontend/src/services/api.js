import axios from 'axios';

const API_URL = 'http://localhost:8000'; // Adjust if backend runs elsewhere

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getEmployees = () => api.get('/employees/');
export const createEmployee = (data) => api.post('/employees/', data);
export const deleteEmployee = (id) => api.delete(`/employees/${id}`);

export const markAttendance = (data) => api.post('/attendance/', data);
export const getAttendance = (employeeId) => api.get(`/attendance/${employeeId}`);

export default api;
