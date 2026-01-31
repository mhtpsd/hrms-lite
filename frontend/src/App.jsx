import { Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Attendance from './pages/Attendance';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Dashboard />} />
      <Route path="/attendance" element={<Attendance />} />
    </Routes>
  );
}

export default App;
