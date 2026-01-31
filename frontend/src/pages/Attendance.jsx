import React, { useEffect, useState } from 'react';
import { getEmployees, markAttendance, getAttendance } from '../services/api';
import Layout from '../components/Layout';

const Attendance = () => {
    const [employees, setEmployees] = useState([]);
    const [selectedEmployee, setSelectedEmployee] = useState('');
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [status, setStatus] = useState('Present');
    const [message, setMessage] = useState('');

    const [viewEmployeeId, setViewEmployeeId] = useState('');
    const [attendanceRecords, setAttendanceRecords] = useState([]);
    const [loadingRecords, setLoadingRecords] = useState(false);

    useEffect(() => {
        fetchEmployees();
    }, []);

    useEffect(() => {
        if (viewEmployeeId) {
            fetchAttendance(viewEmployeeId);
        } else {
            setAttendanceRecords([]);
        }
    }, [viewEmployeeId]);

    const fetchEmployees = async () => {
        try {
            const response = await getEmployees();
            setEmployees(response.data);
        } catch (err) {
            console.error("Failed to fetch employees", err);
        }
    };

    const fetchAttendance = async (empId) => {
        setLoadingRecords(true);
        try {
            const response = await getAttendance(empId);
            setAttendanceRecords(response.data);
        } catch (err) {
            console.error("Failed to fetch attendance", err);
        } finally {
            setLoadingRecords(false);
        }
    };

    const handleMarkAttendance = async (e) => {
        e.preventDefault();
        if (!selectedEmployee) {
            setMessage('Please select an employee');
            return;
        }
        try {
            // Find internal ID if validation needs it, but value should be internal ID
            await markAttendance({
                employee_id: parseInt(selectedEmployee),
                date: date,
                status: status
            });
            setMessage('Attendance marked successfully!');
            if (viewEmployeeId === selectedEmployee) {
                fetchAttendance(selectedEmployee);
            }
            setTimeout(() => setMessage(''), 3000);
        } catch (err) {
            setMessage('Failed to mark attendance: ' + (err.response?.data?.detail || err.message));
        }
    };

    return (
        <Layout>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Mark Attendance Section */}
                <div className="bg-white shadow rounded-lg p-6">
                    <h2 className="text-xl font-bold mb-4 text-gray-800">Mark Attendance</h2>
                    {message && (
                        <div className={`mb-4 px-4 py-2 rounded ${message.includes('Success') || message.includes('success') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                            {message}
                        </div>
                    )}
                    <form onSubmit={handleMarkAttendance}>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2">Employee</label>
                            <select
                                className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                value={selectedEmployee}
                                onChange={(e) => setSelectedEmployee(e.target.value)}
                                required
                            >
                                <option value="">Select Employee</option>
                                {employees.map(emp => (
                                    <option key={emp.id} value={emp.id}>{emp.name} ({emp.employee_id})</option>
                                ))}
                            </select>
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 text-sm font-bold mb-2">Date</label>
                            <input
                                type="date"
                                className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                value={date}
                                onChange={(e) => setDate(e.target.value)}
                                required
                            />
                        </div>
                        <div className="mb-6">
                            <label className="block text-gray-700 text-sm font-bold mb-2">Status</label>
                            <select
                                className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                value={status}
                                onChange={(e) => setStatus(e.target.value)}
                            >
                                <option value="Present">Present</option>
                                <option value="Absent">Absent</option>
                            </select>
                        </div>
                        <button
                            type="submit"
                            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                        >
                            Mark Attendance
                        </button>
                    </form>
                </div>

                {/* View Attendance Section */}
                <div className="bg-white shadow rounded-lg p-6">
                    <h2 className="text-xl font-bold mb-4 text-gray-800">Attendance History</h2>
                    <div className="mb-4">
                        <label className="block text-gray-700 text-sm font-bold mb-2">Select Employee to View</label>
                        <select
                            className="shadow border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            value={viewEmployeeId}
                            onChange={(e) => setViewEmployeeId(e.target.value)}
                        >
                            <option value="">Select Employee</option>
                            {employees.map(emp => (
                                <option key={emp.id} value={emp.id}>{emp.name} ({emp.employee_id})</option>
                            ))}
                        </select>
                    </div>

                    <div className="overflow-y-auto max-h-96">
                        {loadingRecords ? (
                            <div className="text-center py-4">Loading...</div>
                        ) : attendanceRecords.length > 0 ? (
                            <table className="min-w-full divide-y divide-gray-200">
                                <thead className="bg-gray-50">
                                    <tr>
                                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="bg-white divide-y divide-gray-200">
                                    {attendanceRecords.map((record) => (
                                        <tr key={record.id}>
                                            <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">{record.date}</td>
                                            <td className={`px-4 py-2 whitespace-nowrap text-sm font-bold ${record.status === 'Present' ? 'text-green-600' : 'text-red-600'}`}>
                                                {record.status}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        ) : (
                            <div className="text-center py-4 text-gray-500">
                                {viewEmployeeId ? 'No records found.' : 'Select an employee to view records.'}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default Attendance;
