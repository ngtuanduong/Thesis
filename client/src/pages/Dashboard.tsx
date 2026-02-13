import { Row, Col, Card, Statistic, Typography } from 'antd';
import {
  CodeOutlined,
  CheckCircleOutlined,
  TrophyOutlined,
  BookOutlined,
} from '@ant-design/icons';

const { Title } = Typography;

function Dashboard() {
  return (
    <div>
      <Title level={3}>Dashboard</Title>
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Problems Solved"
              value={0}
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Submissions"
              value={0}
              prefix={<CodeOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Current Streak"
              value={0}
              suffix="days"
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#cf1322' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Enrolled Courses"
              value={0}
              prefix={<BookOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col xs={24} lg={12}>
          <Card title="Recommended Problems">
            <p>Complete your profile to get personalized recommendations.</p>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="Recent Activity">
            <p>No recent activity yet. Start solving problems!</p>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default Dashboard;
