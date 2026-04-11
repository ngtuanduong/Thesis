import { lazy, Suspense } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Spin } from 'antd';
import DashboardLayout from '../layouts/DashboardLayout';
import AuthLayout from '../layouts/AuthLayout';
import { useMe } from '../api/queries/useAuth';

const Login = lazy(() => import('../pages/Login'));
const Dashboard = lazy(() => import('../pages/Dashboard'));
const Problems = lazy(() => import('../pages/Problems'));
const ProblemDetail = lazy(() => import('../pages/ProblemDetail'));
const Profile = lazy(() => import('../pages/Profile'));
const KnowledgeMap = lazy(() => import('../pages/KnowledgeMap'));
const ReviewQueue = lazy(() => import('../pages/ReviewQueue'));
const InstructorDashboard = lazy(() => import('../pages/InstructorDashboard'));
const ProblemManage = lazy(() => import('../pages/ProblemManage'));
const ConceptManage = lazy(() => import('../pages/ConceptManage'));
const Glossary = lazy(() => import('../pages/Glossary'));
const Courses = lazy(() => import('../pages/Courses'));
const CourseManage = lazy(() => import('../pages/CourseManage'));
const AdminDashboard = lazy(() => import('../pages/AdminDashboard'));
const Survey = lazy(() => import('../pages/Survey'));

const PageLoader = () => (
  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: 200 }}>
    <Spin size="large" />
  </div>
);

function AppRoutes() {
  const { data: user, isLoading } = useMe();
  const isAuthenticated = !!user;

  if (isLoading) {
    return null;
  }

  return (
    <Suspense fallback={<PageLoader />}>
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
          <Route path="/knowledge-map" element={<KnowledgeMap />} />
          <Route path="/review-queue" element={<ReviewQueue />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/glossary" element={<Glossary />} />
          <Route path="/instructor" element={<InstructorDashboard />} />
          <Route path="/instructor/problems" element={<ProblemManage />} />
          <Route path="/instructor/concepts" element={<ConceptManage />} />
          <Route path="/instructor/courses" element={<CourseManage />} />
          <Route path="/admin" element={<AdminDashboard />} />
          <Route path="/survey" element={<Survey />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Suspense>
  );
}

export default AppRoutes;
