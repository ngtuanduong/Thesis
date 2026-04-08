import { useState, useMemo } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, theme, Avatar, Dropdown } from 'antd';
import type { MenuProps } from 'antd';
import {
  DashboardOutlined,
  CodeOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  NodeIndexOutlined,
  CalendarOutlined,
  TeamOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import { useMe } from '../api/queries/useAuth';
import ErrorBoundary from '../components/ErrorBoundary';

const { Header, Sider, Content } = Layout;

function DashboardLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { token: themeToken } = theme.useToken();
  const { data: user } = useMe();

  const menuItems: MenuProps['items'] = useMemo(() => {
    const items: MenuProps['items'] = [
      { key: '/', icon: <DashboardOutlined />, label: 'Dashboard' },
      { key: '/problems', icon: <CodeOutlined />, label: 'Problems' },
      { key: '/knowledge-map', icon: <NodeIndexOutlined />, label: 'Knowledge Map' },
      { key: '/review-queue', icon: <CalendarOutlined />, label: 'Review Queue' },
      { key: '/profile', icon: <UserOutlined />, label: 'Profile' },
    ];

    if (user?.role === 'INSTRUCTOR' || user?.role === 'ADMIN') {
      items.push(
        { type: 'divider' },
        { key: '/instructor', icon: <TeamOutlined />, label: 'Instructor' },
        { key: '/instructor/problems', icon: <CodeOutlined />, label: 'Manage Problems' },
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
      <Sider trigger={null} collapsible collapsed={collapsed}>
        <div
          style={{
            height: 64,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#fff',
            fontSize: collapsed ? 16 : 20,
            fontWeight: 700,
          }}
        >
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
      <Layout>
        <Header
          style={{
            padding: '0 24px',
            background: themeToken.colorBgContainer,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          {collapsed ? (
            <MenuUnfoldOutlined onClick={() => setCollapsed(false)} style={{ fontSize: 18 }} />
          ) : (
            <MenuFoldOutlined onClick={() => setCollapsed(true)} style={{ fontSize: 18 }} />
          )}
          <Dropdown menu={userMenu} placement="bottomRight">
            <Avatar icon={<UserOutlined />} style={{ cursor: 'pointer' }} />
          </Dropdown>
        </Header>
        <Content
          style={{
            margin: 24,
            padding: 24,
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
