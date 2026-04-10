import {
  Card,
  Typography,
  Spin,
  Empty,
  Tag,
  List,
  Progress,
  Row,
  Col,
  Statistic,
  Badge,
  Button,
} from 'antd';
import {
  ClockCircleOutlined,
  WarningOutlined,
  CalendarOutlined,
  ThunderboltOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useMe } from '../api/queries/useAuth';
import { useReviewQueue, useAdaptiveRecommendations } from '../api/queries/useAdaptive';
import type { ReviewItem } from '../types';
import { useResponsive } from '../hooks/useResponsive';

const { Title, Text } = Typography;

function getRetrievabilityColor(r: number): string {
  if (r < 0.5) return '#f5222d';
  if (r < 0.7) return '#fa8c16';
  if (r < 0.9) return '#1890ff';
  return '#52c41a';
}

function getRetrievabilityLabel(r: number): string {
  if (r < 0.5) return 'Critical';
  if (r < 0.7) return 'Fading';
  if (r < 0.9) return 'Good';
  return 'Strong';
}

function formatDueDate(dateStr: string): string {
  const due = new Date(dateStr);
  const now = new Date();
  const diffMs = due.getTime() - now.getTime();
  const diffHours = Math.round(diffMs / (1000 * 60 * 60));
  const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

  if (diffMs < 0) {
    const overdue = Math.abs(diffDays);
    return overdue === 0 ? 'Overdue today' : `${overdue}d overdue`;
  }
  if (diffHours < 24) return `In ${Math.max(1, diffHours)}h`;
  if (diffDays < 7) return `In ${diffDays}d`;
  return due.toLocaleDateString();
}

function ReviewItemCard({ item, showActions = true }: { item: ReviewItem; showActions?: boolean }) {
  const navigate = useNavigate();
  const { isMobile } = useResponsive();
  const rColor = getRetrievabilityColor(item.retrievability);
  const rLabel = getRetrievabilityLabel(item.retrievability);

  return (
    <List.Item
      actions={
        showActions
          ? [
              <Button
                type="link"
                size="small"
                onClick={() => navigate('/problems')}
              >
                Practice
              </Button>,
            ]
          : undefined
      }
    >
      <List.Item.Meta
        title={
          <span>
            {item.display_name}
            <Tag
              color={rColor}
              style={{ marginLeft: 8 }}
            >
              {rLabel}
            </Tag>
            <Tag>{item.state}</Tag>
          </span>
        }
        description={
          <Row gutter={16}>
            <Col>
              <Text type="secondary" style={{ fontSize: 12 }}>
                <ClockCircleOutlined style={{ marginRight: 4 }} />
                {formatDueDate(item.due_date)}
              </Text>
            </Col>
            <Col>
              <Text type="secondary" style={{ fontSize: 12 }}>
                Memory: {(item.retrievability * 100).toFixed(0)}%
              </Text>
            </Col>
            <Col>
              <Text type="secondary" style={{ fontSize: 12 }}>
                Stability: {item.stability.toFixed(1)}d
              </Text>
            </Col>
          </Row>
        }
      />
      <div style={{ width: isMobile ? 48 : 60 }}>
        <Progress
          type="circle"
          percent={Math.round(item.retrievability * 100)}
          size={44}
          strokeColor={rColor}
          format={(pct) => `${pct}`}
        />
      </div>
    </List.Item>
  );
}

function ReviewQueue() {
  const { data: user } = useMe();
  const { data: reviewData, isLoading: reviewLoading } = useReviewQueue(user?.id);
  const { data: recData, isLoading: recLoading } = useAdaptiveRecommendations(user?.id, 5);
  const navigate = useNavigate();

  if (reviewLoading) {
    return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />;
  }

  const dueNow = reviewData?.due_now || [];
  const upcoming = reviewData?.upcoming || [];
  const criticalCount = dueNow.filter((r) => r.retrievability < 0.7).length;

  return (
    <div>
      <Title level={3}>
        <CalendarOutlined style={{ marginRight: 8 }} />
        Review Queue
      </Title>

      {/* Summary Stats */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Due Now"
              value={dueNow.length}
              prefix={
                <Badge count={criticalCount} size="small" offset={[4, 0]}>
                  <ThunderboltOutlined style={{ color: '#fa8c16' }} />
                </Badge>
              }
              valueStyle={{ color: dueNow.length > 0 ? '#cf1322' : '#3f8600' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Critical"
              value={criticalCount}
              prefix={<WarningOutlined />}
              valueStyle={{ color: criticalCount > 0 ? '#f5222d' : '#999' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Upcoming"
              value={upcoming.length}
              prefix={<CalendarOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Avg Memory"
              value={
                dueNow.length > 0
                  ? Math.round(
                      (dueNow.reduce((s, r) => s + r.retrievability, 0) /
                        dueNow.length) *
                        100,
                    )
                  : 100
              }
              suffix="%"
              valueStyle={{
                color:
                  dueNow.length > 0 &&
                  dueNow.reduce((s, r) => s + r.retrievability, 0) /
                    dueNow.length <
                    0.7
                    ? '#cf1322'
                    : '#3f8600',
              }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        {/* Due Now */}
        <Col xs={24} lg={12}>
          <Card
            title={
              <span>
                <ThunderboltOutlined style={{ color: '#fa8c16', marginRight: 8 }} />
                Due for Review
              </span>
            }
            extra={
              <Tag color={dueNow.length > 0 ? 'red' : 'green'}>
                {dueNow.length} items
              </Tag>
            }
          >
            {dueNow.length === 0 ? (
              <Empty description="All caught up! No reviews due right now." />
            ) : (
              <List
                dataSource={dueNow}
                renderItem={(item) => <ReviewItemCard item={item} />}
              />
            )}
          </Card>
        </Col>

        {/* Upcoming */}
        <Col xs={24} lg={12}>
          <Card
            title={
              <span>
                <CalendarOutlined style={{ color: '#1890ff', marginRight: 8 }} />
                Upcoming Reviews
              </span>
            }
            extra={
              <Tag color="blue">{upcoming.length} items</Tag>
            }
          >
            {upcoming.length === 0 ? (
              <Empty description="No upcoming reviews scheduled." />
            ) : (
              <List
                dataSource={upcoming}
                renderItem={(item) => (
                  <ReviewItemCard item={item} showActions={false} />
                )}
              />
            )}
          </Card>
        </Col>
      </Row>

      {/* Adaptive Recommendations */}
      <Card
        title="Recommended Next Problems"
        extra={<Text type="secondary">Powered by Adaptive Engine</Text>}
        style={{ marginTop: 16 }}
      >
        {recLoading ? (
          <div style={{ textAlign: 'center', padding: 20 }}>
            <Spin />
          </div>
        ) : !recData?.recommendations || recData.recommendations.length === 0 ? (
          <Empty description="Solve problems to get adaptive recommendations!" />
        ) : (
          <List
            dataSource={recData.recommendations}
            renderItem={(rec) => (
              <List.Item
                style={{ cursor: 'pointer' }}
                onClick={() => navigate(`/problems/${rec.problem_id}`)}
                actions={[
                  <Tag color="blue">{rec.concept_display_name}</Tag>,
                ]}
              >
                <List.Item.Meta
                  title={
                    <span>
                      {rec.title}{' '}
                      <Tag
                        color={
                          rec.difficulty === 'EASY'
                            ? 'green'
                            : rec.difficulty === 'MEDIUM'
                              ? 'orange'
                              : 'red'
                        }
                      >
                        {rec.difficulty}
                      </Tag>
                    </span>
                  }
                  description={rec.reason}
                />
              </List.Item>
            )}
          />
        )}
      </Card>
    </div>
  );
}

export default ReviewQueue;
