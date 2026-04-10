import { Outlet } from 'react-router-dom';
import { Layout, Typography } from 'antd';
import { useResponsive } from '../hooks/useResponsive';

const { Content } = Layout;
const { Title } = Typography;

function AuthLayout() {
  const { isMobile } = useResponsive();

  return (
    <Layout
      style={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: '#f0f2f5',
      }}
    >
      <Content
        style={{
          width: '100%',
          maxWidth: 420,
          padding: isMobile ? '24px 16px' : '40px 24px',
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <Title level={2}>Adaptive Learning Platform</Title>
        </div>
        <Outlet />
      </Content>
    </Layout>
  );
}

export default AuthLayout;
