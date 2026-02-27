import { Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from '../layouts/DashboardLayout';
import AuthLayout from '../layouts/AuthLayout';
import Login from '../pages/Login';
import Dashboard from '../pages/Dashboard';
import Problems from '../pages/Problems';
import ProblemDetail from '../pages/ProblemDetail';
import Profile from '../pages/Profile';
import { useMe } from '../api/queries/useAuth';

function AppRoutes() {
  const { data: user, isLoading } = useMe();
  const isAuthenticated = !!user;

  if (isLoading) {
    return null;
  }

  return (
    <Routes>
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
      </Route>

      <Route
        element={isAuthenticated ? <DashboardLayout /> : <Navigate to="/login" replace />}
      >
        <Route path="/" element={<Dashboard />} />
        <Route path="/problems" element={<Problems />} />
        <Route path="/problems/:id" element={<ProblemDetail />} />
        <Route path="/profile" element={<Profile />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default AppRoutes;
