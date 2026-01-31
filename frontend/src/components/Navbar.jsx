import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
    const location = useLocation();

    const isActive = (path) => location.pathname === path;

    return (
        <nav className="bg-indigo-600 shadow-lg">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    <div className="flex items-center">
                        <div className="flex-shrink-0">
                            <span className="text-white text-xl font-bold">HRMS Lite</span>
                        </div>
                        <div className="hidden md:block">
                            <div className="ml-10 flex items-baseline space-x-4">
                                <Link
                                    to="/"
                                    className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/') ? 'bg-indigo-700 text-white' : 'text-white hover:bg-indigo-500'
                                        }`}
                                >
                                    Dashboard
                                </Link>
                                <Link
                                    to="/attendance"
                                    className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/attendance') ? 'bg-indigo-700 text-white' : 'text-white hover:bg-indigo-500'
                                        }`}
                                >
                                    Attendance
                                </Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
