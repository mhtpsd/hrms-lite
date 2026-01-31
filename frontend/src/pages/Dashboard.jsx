import React, { useEffect, useState } from 'react';
import { getEmployees, createEmployee, deleteEmployee } from '../services/api';
import EmployeeList from '../components/EmployeeList';
import EmployeeForm from '../components/EmployeeForm';
import Layout from '../components/Layout';

const Dashboard = () => {
    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showForm, setShowForm] = useState(false);

    const fetchEmployees = async () => {
        try {
            setLoading(true);
            const response = await getEmployees();
            setEmployees(response.data);
            setError(null);
        } catch (err) {
            setError('Failed to fetch employees. Is the backend running?');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchEmployees();
    }, []);

    const handleAddEmployee = async (employeeData) => {
        try {
            await createEmployee(employeeData);
            setShowForm(false);
            fetchEmployees();
        } catch (err) {
            alert(err.response?.data?.detail || 'Failed to create employee');
        }
    };

    const handleDeleteEmployee = async (id) => {
        if (window.confirm('Are you sure you want to delete this employee?')) {
            try {
                await deleteEmployee(id);
                fetchEmployees();
            } catch (err) {
                alert('Failed to delete employee');
            }
        }
    };

    return (
        <Layout>
            <div className="px-4 sm:px-0">
                <div className="flex justify-between items-center mb-6">
                    <h1 className="text-2xl font-semibold text-gray-900">Employee Management</h1>
                    <button
                        onClick={() => setShowForm(true)}
                        className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                    >
                        Add Employee
                    </button>
                </div>

                {error && (
                    <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4" role="alert">
                        <strong className="font-bold">Error: </strong>
                        <span className="block sm:inline">{error}</span>
                    </div>
                )}

                {loading ? (
                    <div className="flex justify-center items-center h-32">
                        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
                    </div>
                ) : (
                    <EmployeeList employees={employees} onDelete={handleDeleteEmployee} />
                )}

                {showForm && (
                    <EmployeeForm onSubmit={handleAddEmployee} onClose={() => setShowForm(false)} />
                )}
            </div>
        </Layout>
    );
};

export default Dashboard;
