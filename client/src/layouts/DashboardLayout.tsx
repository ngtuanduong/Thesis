import { useState, useMemo, useEffect } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, theme, Avatar, Dropdown, Drawer } from 'antd';
import type { MenuProps } from 'antd';
import {
  DashboardOutlined,
  CodeOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  MenuOutlined,
  NodeIndexOutlined,
  CalendarOutlined,
  TeamOutlined,
  SettingOutlined,
  BookOutlined,
} from '@ant-design/icons';
import { useMe } from '../api/queries/useAuth';
import ErrorBoundary from '../components/ErrorBoundary';
import HelpMenu from '../components/onboarding/HelpMenu';
import { useResponsive } from '../hooks/useResponsive';
import styles from './DashboardLayout.module.css';

const { Header, Sider, Content } = Layout;

function DashboardLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { token: themeToken } = theme.useToken();
  const { data: user } = useMe();
  const { isMobile } = useResponsive();

  useEffect(() => {
    if (isMobile) setDrawerOpen(false);
  }, [location.pathname, isMobile]);

  const menuItems: MenuProps['items'] = useMemo(() => {
    const items: MenuProps['items'] = [
      { key: '/', icon: <DashboardOutlined />, label: 'Dashboard' },
      { key: '/problems', icon: <CodeOutlined />, label: 'Problems' },
      { key: '/knowledge-map', icon: <NodeIndexOutlined />, label: 'Knowledge Map' },
      { key: '/review-queue', icon: <CalendarOutlined />, label: 'Review Queue' },
      { key: '/profile', icon: <UserOutlined />, label: 'Profile' },
      { key: '/glossary', icon: <BookOutlined />, label: 'Glossary' },
    ];

    if (user?.role === 'INSTRUCTOR' || user?.role === 'ADMIN') {
      items.push(
        { type: 'divider' },
        { key: '/instructor', icon: <TeamOutlined />, label: 'Instructor' },
        { key: '/instructor/problems', icon: <CodeOutlined />, label: 'Manage Problems' },
        { key: '/instructor/concepts', icon: <NodeIndexOutlined />, label: 'Manage Concepts' },
      );
    }

    if (user?.role === 'ADMIN') {
      items.push(
        { key: '/admin', icon: <SettingOutlined />, label: 'Admin' },
      );
    }

    return items;
  }, [user?.role]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const userMenu = {
    items: [
      { key: 'profile', icon: <UserOutlined />, label: 'Profile', onClick: () => navigate('/profile') },
      { type: 'divider' as const },
      { key: 'survey', label: 'Take Survey', onClick: () => navigate('/survey') },
      { key: 'logout', icon: <LogoutOutlined />, label: 'Logout', onClick: handleLogout },
    ],
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      {isMobile ? (
        <Drawer
          placement="left"
          open={drawerOpen}
          onClose={() => setDrawerOpen(false)}
          width={256}
          styles={{ body: { padding: 0, background: '#001529' } }}
        >
          <div className={styles.sidebarLogo} style={{ fontSize: 20 }}>
            AdaptLearn
          </div>
          <Menu
            theme="dark"
            mode="inline"
            selectedKeys={[location.pathname]}
            items={menuItems}
            onClick={({ key }) => {
              navigate(key);
              setDrawerOpen(false);
            }}
          />
        </Drawer>
      ) : (
        <Sider trigger={null} collapsible collapsed={collapsed} className={styles.sidebar}>
          <div className={styles.sidebarLogo} style={{ fontSize: collapsed ? 16 : 20 }}>
            {collapsed ? 'AL' : 'AdaptLearn'}
          </div>
          <Menu
            theme="dark"
            mode="inline"
            selectedKeys={[location.pathname]}
            items={menuItems}
            onClick={({ key }) => navigate(key)}
          />
        </Sider>
      )}
      <Layout>
        <Header
          className={styles.headerBar}
          style={{
            padding: isMobile ? '0 12px' : '0 24px',
            background: themeToken.colorBgContainer,
          }}
        >
          {isMobile ? (
            <MenuOutlined onClick={() => setDrawerOpen(true)} style={{ fontSize: 18 }} />
          ) : collapsed ? (
            <MenuUnfoldOutlined onClick={() => setCollapsed(false)} style={{ fontSize: 18 }} />
          ) : (
            <MenuFoldOutlined onClick={() => setCollapsed(true)} style={{ fontSize: 18 }} />
          )}
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <HelpMenu />
            <Dropdown menu={userMenu} placement="bottomRight">
              <Avatar icon={<UserOutlined />} style={{ cursor: 'pointer' }} />
            </Dropdown>
          </div>
        </Header>
        <Content
          style={{
            margin: isMobile ? 8 : 24,
            padding: isMobile ? 12 : 24,
            background: themeToken.colorBgContainer,
            borderRadius: themeToken.borderRadiusLG,
            minHeight: 280,
          }}
        >
          <ErrorBoundary>
            <Outlet />
          </ErrorBoundary>
        </Content>
      </Layout>
    </Layout>
  );
}

export default DashboardLayout;
