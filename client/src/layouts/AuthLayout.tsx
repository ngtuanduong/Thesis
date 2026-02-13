import { Outlet } from 'react-router-dom';
import { Layout, Typography } from 'antd';

const { Content } = Layout;
const { Title } = Typography;

function AuthLayout() {
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
          padding: '40px 24px',
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
