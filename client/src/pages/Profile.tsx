import { Card, Typography, Descriptions, Spin } from 'antd';
import { useMe } from '../api/queries/useAuth';

const { Title } = Typography;

function Profile() {
  const { data: user, isLoading } = useMe();

  if (isLoading) {
    return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />;
  }

  return (
    <div>
      <Title level={3}>Profile</Title>
      <Card style={{ marginTop: 16 }}>
        <Descriptions column={1} bordered>
          <Descriptions.Item label="Name">{user?.name || 'N/A'}</Descriptions.Item>
          <Descriptions.Item label="Email">{user?.email || 'N/A'}</Descriptions.Item>
          <Descriptions.Item label="Role">{user?.role || 'N/A'}</Descriptions.Item>
        </Descriptions>
      </Card>

      <Card title="Skill Visualization" style={{ marginTop: 16 }}>
        <p>Skill radar chart will be displayed here once you solve problems.</p>
      </Card>
    </div>
  );
}

export default Profile;
