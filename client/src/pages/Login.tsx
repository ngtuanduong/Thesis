import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Button, Typography, message, Tabs } from 'antd';
import { MailOutlined, LockOutlined, UserOutlined } from '@ant-design/icons';
import { useLogin, useRegister } from '../api/queries/useAuth';

const { Text } = Typography;

function Login() {
  const [activeTab, setActiveTab] = useState('login');
  const navigate = useNavigate();
  const login = useLogin();
  const register = useRegister();

  const onLogin = async (values: { email: string; password: string }) => {
    try {
      await login.mutateAsync(values);
      navigate('/');
    } catch {
      message.error('Invalid email or password');
    }
  };

  const onRegister = async (values: { email: string; password: string; name: string }) => {
    try {
      await register.mutateAsync(values);
      navigate('/');
    } catch {
      message.error('Registration failed. Email may already exist.');
    }
  };

  return (
    <Card>
      <Tabs
        activeKey={activeTab}
        onChange={setActiveTab}
        centered
        items={[
          {
            key: 'login',
            label: 'Login',
            children: (
              <Form layout="vertical" onFinish={onLogin}>
                <Form.Item name="email" rules={[{ required: true, type: 'email' }]}>
                  <Input prefix={<MailOutlined />} placeholder="Email" size="large" />
                </Form.Item>
                <Form.Item name="password" rules={[{ required: true, min: 6 }]}>
                  <Input.Password prefix={<LockOutlined />} placeholder="Password" size="large" />
                </Form.Item>
                <Form.Item>
                  <Button
                    type="primary"
                    htmlType="submit"
                    block
                    size="large"
                    loading={login.isPending}
                  >
                    Login
                  </Button>
                </Form.Item>
                <Text type="secondary">
                  Don't have an account?{' '}
                  <a onClick={() => setActiveTab('register')}>Register now</a>
                </Text>
              </Form>
            ),
          },
          {
            key: 'register',
            label: 'Register',
            children: (
              <Form layout="vertical" onFinish={onRegister}>
                <Form.Item name="name" rules={[{ required: true, min: 2 }]}>
                  <Input prefix={<UserOutlined />} placeholder="Full name" size="large" />
                </Form.Item>
                <Form.Item name="email" rules={[{ required: true, type: 'email' }]}>
                  <Input prefix={<MailOutlined />} placeholder="Email" size="large" />
                </Form.Item>
                <Form.Item name="password" rules={[{ required: true, min: 6 }]}>
                  <Input.Password prefix={<LockOutlined />} placeholder="Password" size="large" />
                </Form.Item>
                <Form.Item>
                  <Button
                    type="primary"
                    htmlType="submit"
                    block
                    size="large"
                    loading={register.isPending}
                  >
                    Register
                  </Button>
                </Form.Item>
              </Form>
            ),
          },
        ]}
      />
    </Card>
  );
}

export default Login;
