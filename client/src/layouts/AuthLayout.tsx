import { Outlet } from 'react-router-dom';
import { Layout, Typography } from 'antd';
import { useResponsive } from '../hooks/useResponsive';
import styles from './AuthLayout.module.css';

const { Content } = Layout;
const { Title } = Typography;

function AuthLayout() {
  const { isMobile } = useResponsive();

  return (
    <Layout className={styles.wrapper}>
      <Content
        className={styles.content}
        style={{ padding: isMobile ? '24px 16px' : '40px 24px' }}
      >
        <div className={styles.titleBlock}>
          <Title level={2}>Adaptive Learning Platform</Title>
        </div>
        <Outlet />
      </Content>
    </Layout>
  );
}

export default AuthLayout;
