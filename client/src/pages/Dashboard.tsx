import { Row, Col, Card, Statistic, Typography, List, Tag, Spin, Empty, Progress } from 'antd';
import {
  CodeOutlined,
  CheckCircleOutlined,
  TrophyOutlined,
  BookOutlined,
  ClockCircleOutlined,
  NodeIndexOutlined,
  ThunderboltOutlined,
} from '@ant-design/icons';
import { useDashboardStats, useRecentSubmissions, useRecommendations } from '../api/queries/useDashboard';
import { useKnowledgeState, useReviewQueue, useAdaptiveRecommendations } from '../api/queries/useAdaptive';
import { useMe } from '../api/queries/useAuth';
import { useNavigate } from 'react-router-dom';

const { Title, Text } = Typography;

const difficultyColors: Record<string, string> = {
  EASY: 'green',
  MEDIUM: 'orange',
  HARD: 'red',
};

const statusColors: Record<string, string> = {
  ACCEPTED: 'success',
  WRONG_ANSWER: 'error',
  TIME_LIMIT: 'warning',
  RUNTIME_ERROR: 'error',
  PENDING: 'processing',
  RUNNING: 'processing',
};

function Dashboard() {
  const navigate = useNavigate();
  const { data: user } = useMe();
  const { data: stats, isLoading: statsLoading } = useDashboardStats();
  const { data: recentSubmissions, isLoading: submissionsLoading } = useRecentSubmissions(5);
  const { data: recommendations, isLoading: recommendationsLoading } = useRecommendations(5);
  const { data: knowledgeState } = useKnowledgeState(user?.id);
  const { data: reviewData } = useReviewQueue(user?.id);
  const { data: adaptiveRecs } = useAdaptiveRecommendations(user?.id, 3);

  return (
    <div>
      <Title level={3}>Dashboard</Title>

      {/* Statistics Cards */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Problems Solved"
              value={statsLoading ? 0 : stats?.problemsSolved}
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#3f8600' }}
              loading={statsLoading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Submissions"
              value={statsLoading ? 0 : stats?.totalSubmissions}
              prefix={<CodeOutlined />}
              loading={statsLoading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Active Days"
              value={statsLoading ? 0 : stats?.currentStreak}
              suffix="days"
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#cf1322' }}
              loading={statsLoading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Enrolled Courses"
              value={statsLoading ? 0 : stats?.enrolledCourses}
              prefix={<BookOutlined />}
              loading={statsLoading}
            />
          </Card>
        </Col>
      </Row>

      {/* Adaptive Learning Overview */}
      {knowledgeState?.summary && (
        <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
          <Col xs={24} sm={8}>
            <Card
              hoverable
              onClick={() => navigate('/knowledge-map')}
              style={{ cursor: 'pointer' }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
                <Progress
                  type="circle"
                  percent={Math.round(knowledgeState.summary.overall_mastery * 100)}
                  size={64}
                  strokeColor={{
                    '0%': '#108ee9',
                    '100%': '#87d068',
                  }}
                />
                <div>
                  <Text strong>Knowledge Mastery</Text>
                  <br />
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    {knowledgeState.summary.mastered}/{knowledgeState.summary.total_concepts} concepts mastered
                  </Text>
                </div>
              </div>
            </Card>
          </Col>
          <Col xs={24} sm={8}>
            <Card
              hoverable
              onClick={() => navigate('/review-queue')}
              style={{ cursor: 'pointer' }}
            >
              <Statistic
                title="Reviews Due"
                value={reviewData?.due_now?.length || 0}
                prefix={<ThunderboltOutlined />}
                valueStyle={{
                  color: (reviewData?.due_now?.length || 0) > 0 ? '#cf1322' : '#3f8600',
                }}
                suffix={
                  <Text type="secondary" style={{ fontSize: 14 }}>
                    {' '}concepts
                  </Text>
                }
              />
            </Card>
          </Col>
          <Col xs={24} sm={8}>
            <Card
              hoverable
              onClick={() => navigate('/knowledge-map')}
              style={{ cursor: 'pointer' }}
            >
              <Statistic
                title="Learning Progress"
                value={knowledgeState.summary.learning}
                prefix={<NodeIndexOutlined />}
                valueStyle={{ color: '#1890ff' }}
                suffix={
                  <Text type="secondary" style={{ fontSize: 14 }}>
                    {' '}in progress
                  </Text>
                }
              />
            </Card>
          </Col>
        </Row>
      )}

      {/* Recommendations and Recent Activity */}
      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col xs={24} lg={12}>
          <Card
            title="Recommended Problems"
            extra={<Text type="secondary">Adaptive Engine</Text>}
          >
            {adaptiveRecs?.recommendations && adaptiveRecs.recommendations.length > 0 ? (
              <List
                dataSource={adaptiveRecs.recommendations}
                renderItem={(rec: any) => (
                  <List.Item
                    style={{ cursor: 'pointer' }}
                    onClick={() => navigate(`/problems/${rec.problem_id}`)}
                  >
                    <List.Item.Meta
                      title={
                        <span>
                          {rec.title}{' '}
                          <Tag color={difficultyColors[rec.difficulty]}>
                            {rec.difficulty}
                          </Tag>
                        </span>
                      }
                      description={
                        <span>
                          <Tag color="blue" style={{ marginRight: 4 }}>
                            {rec.concept_display_name}
                          </Tag>
                          <Text type="secondary" style={{ fontSize: 12 }}>
                            {rec.reason}
                          </Text>
                        </span>
                      }
                    />
                  </List.Item>
                )}
              />
            ) : recommendationsLoading ? (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                <Spin />
              </div>
            ) : !recommendations || recommendations.length === 0 ? (
              <Empty description="Solve a problem to get personalized recommendations!" />
            ) : (
              <List
                dataSource={recommendations}
                renderItem={(problem: any) => (
                  <List.Item
                    style={{ cursor: 'pointer' }}
                    onClick={() => navigate(`/problems/${problem.id}`)}
                  >
                    <List.Item.Meta
                      title={
                        <span>
                          {problem.title}{' '}
                          <Tag color={difficultyColors[problem.difficulty]}>
                            {problem.difficulty}
                          </Tag>
                        </span>
                      }
                      description={
                        problem.tags && problem.tags.length > 0
                          ? problem.tags.slice(0, 3).map((tag: string) => (
                              <Tag key={tag} style={{ marginRight: 4 }}>
                                {tag}
                              </Tag>
                            ))
                          : null
                      }
                    />
                  </List.Item>
                )}
              />
            )}
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card title="📊 Recent Activity">
            {submissionsLoading ? (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                <Spin />
              </div>
            ) : !recentSubmissions || recentSubmissions.length === 0 ? (
              <Empty description="No recent activity yet. Start solving problems!" />
            ) : (
              <List
                dataSource={recentSubmissions}
                renderItem={(submission: any) => (
                  <List.Item>
                    <List.Item.Meta
                      title={
                        <span>
                          {submission.problem?.title || 'Unknown Problem'}{' '}
                          <Tag color={statusColors[submission.status]}>
                            {submission.status.replace('_', ' ')}
                          </Tag>
                        </span>
                      }
                      description={
                        <span>
                          <ClockCircleOutlined style={{ marginRight: 4 }} />
                          {new Date(submission.createdAt).toLocaleDateString()}{' '}
                          {submission.runtime && `• ${submission.runtime}ms`}
                        </span>
                      }
                    />
                  </List.Item>
                )}
              />
            )}
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default Dashboard;
