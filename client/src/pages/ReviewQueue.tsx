import { useRef, useState, useMemo } from 'react';
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
  Tabs,
  Table,
  Input,
  Select,
  Space,
} from 'antd';
import {
  ClockCircleOutlined,
  WarningOutlined,
  CalendarOutlined,
  ThunderboltOutlined,
  SearchOutlined,
  BookOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useNavigate } from 'react-router-dom';
import { useMe } from '../api/queries/useAuth';
import { useReviewQueue, useReviewCards } from '../api/queries/useAdaptive';
import type { ReviewItem, ReviewCard } from '../types';
import { useResponsive } from '../hooks/useResponsive';
import PageTour from '../components/onboarding/PageTour';
import TermTooltip from '../components/onboarding/TermTooltip';
import GuidedEmptyState from '../components/onboarding/GuidedEmptyState';

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

function formatRelativeTime(dateStr: string | null): string {
  if (!dateStr) return 'Never';
  const date = new Date(dateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffHours = Math.round(diffMs / (1000 * 60 * 60));
  const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

  if (diffHours < 1) return 'Just now';
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  if (diffDays < 30) return `${Math.round(diffDays / 7)}w ago`;
  return date.toLocaleDateString();
}

const stateColorMap: Record<string, string> = {
  LEARNING: 'blue',
  REVIEW: 'green',
  RELEARNING: 'orange',
};

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

/* ── Tab 1: Review Queue (existing) ── */
function ReviewQueueTab({
  reviewData,
  summaryRef,
  dueRef,
  upcomingRef,
}: {
  reviewData: { due_now: ReviewItem[]; upcoming: ReviewItem[] } | undefined;
  summaryRef: React.Ref<HTMLDivElement>;
  dueRef: React.Ref<HTMLDivElement>;
  upcomingRef: React.Ref<HTMLDivElement>;
}) {
  const dueNow = reviewData?.due_now || [];
  const upcoming = reviewData?.upcoming || [];
  const criticalCount = dueNow.filter((r) => r.retrievability < 0.7).length;

  return (
    <>
      {/* Summary Stats */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }} ref={summaryRef}>
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
              title={<TermTooltip term="retrievability">Avg Memory</TermTooltip>}
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
        <Col xs={24} lg={12} ref={dueRef}>
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
        <Col xs={24} lg={12} ref={upcomingRef}>
          <Card
            title={
              <span>
                <CalendarOutlined style={{ color: '#1890ff', marginRight: 8 }} />
                <TermTooltip term="spaced_repetition">Upcoming Reviews</TermTooltip>
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
    </>
  );
}

/* ── Tab 2: All Concepts Browser ── */
function AllConceptsView({ userId }: { userId?: string }) {
  const navigate = useNavigate();
  const { isMobile } = useResponsive();
  const { data: cards, isLoading } = useReviewCards(userId);

  const [searchText, setSearchText] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [stateFilter, setStateFilter] = useState<string>('all');
  const [topicFilter, setTopicFilter] = useState<string>('all');

  const topicGroups = useMemo(() => {
    if (!cards) return [];
    const groups = new Set(cards.map((c) => c.topic_group).filter(Boolean));
    return Array.from(groups).sort();
  }, [cards]);

  const filteredCards = useMemo(() => {
    if (!cards) return [];
    return cards.filter((card) => {
      if (searchText && !card.display_name.toLowerCase().includes(searchText.toLowerCase())) return false;
      if (statusFilter !== 'all' && card.memory_status !== statusFilter) return false;
      if (stateFilter !== 'all' && card.state !== stateFilter) return false;
      if (topicFilter !== 'all' && card.topic_group !== topicFilter) return false;
      return true;
    });
  }, [cards, searchText, statusFilter, stateFilter, topicFilter]);

  const stats = useMemo(() => {
    if (!cards) return { total: 0, strong: 0, good: 0, fading: 0, critical: 0 };
    return {
      total: cards.length,
      strong: cards.filter((c) => c.memory_status === 'strong').length,
      good: cards.filter((c) => c.memory_status === 'good').length,
      fading: cards.filter((c) => c.memory_status === 'fading').length,
      critical: cards.filter((c) => c.memory_status === 'critical').length,
    };
  }, [cards]);

  const columns: ColumnsType<ReviewCard> = [
    {
      title: 'Concept',
      dataIndex: 'display_name',
      sorter: (a, b) => a.display_name.localeCompare(b.display_name),
      render: (name: string, record: ReviewCard) => (
        <div>
          <Text strong>{name}</Text>
          {record.topic_group && (
            <div>
              <Text type="secondary" style={{ fontSize: 12 }}>{record.topic_group}</Text>
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Memory',
      dataIndex: 'retrievability',
      sorter: (a, b) => a.retrievability - b.retrievability,
      defaultSortOrder: 'ascend',
      width: 120,
      render: (r: number) => (
        <Space>
          <Progress
            type="circle"
            percent={Math.round(r * 100)}
            size={36}
            strokeColor={getRetrievabilityColor(r)}
            format={(pct) => `${pct}`}
          />
          <Tag color={getRetrievabilityColor(r)}>{getRetrievabilityLabel(r)}</Tag>
        </Space>
      ),
    },
    {
      title: 'State',
      dataIndex: 'state',
      width: 110,
      filters: [
        { text: 'Learning', value: 'LEARNING' },
        { text: 'Review', value: 'REVIEW' },
        { text: 'Relearning', value: 'RELEARNING' },
      ],
      onFilter: (value, record) => record.state === value,
      render: (state: string) => (
        <Tag color={stateColorMap[state] || 'default'}>{state}</Tag>
      ),
    },
    {
      title: 'Stability',
      dataIndex: 'stability',
      sorter: (a, b) => a.stability - b.stability,
      width: 90,
      responsive: ['md'] as ('md')[],
      render: (s: number) => `${s.toFixed(1)}d`,
    },
    {
      title: 'Reviews',
      dataIndex: 'reps',
      sorter: (a, b) => a.reps - b.reps,
      width: 80,
    },
    {
      title: 'Lapses',
      dataIndex: 'lapses',
      sorter: (a, b) => a.lapses - b.lapses,
      width: 75,
      responsive: ['md'] as ('md')[],
      render: (lapses: number) => (
        <Text style={lapses > 0 ? { color: '#f5222d' } : undefined}>{lapses}</Text>
      ),
    },
    {
      title: 'Last Review',
      dataIndex: 'last_review',
      sorter: (a, b) => {
        const aTime = a.last_review ? new Date(a.last_review).getTime() : 0;
        const bTime = b.last_review ? new Date(b.last_review).getTime() : 0;
        return aTime - bTime;
      },
      width: 110,
      responsive: ['lg'] as ('lg')[],
      render: (date: string | null) => (
        <Text type="secondary" style={{ fontSize: 12 }}>{formatRelativeTime(date)}</Text>
      ),
    },
    {
      title: 'Due Date',
      dataIndex: 'due_date',
      sorter: (a, b) => new Date(a.due_date).getTime() - new Date(b.due_date).getTime(),
      width: 110,
      render: (date: string) => (
        <Text type="secondary" style={{ fontSize: 12 }}>
          <ClockCircleOutlined style={{ marginRight: 4 }} />
          {formatDueDate(date)}
        </Text>
      ),
    },
    {
      title: '',
      key: 'action',
      width: 80,
      render: () => (
        <Button type="link" size="small" onClick={() => navigate('/problems')}>
          Practice
        </Button>
      ),
    },
  ];

  if (isLoading) {
    return <Spin size="large" className="center-spin" />;
  }

  if (!cards || cards.length === 0) {
    return (
      <div style={{ marginTop: 16 }}>
        <GuidedEmptyState type="reviews" />
      </div>
    );
  }

  return (
    <div>
      {/* Summary Stats */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={12} sm={4}>
          <Card>
            <Statistic
              title="Total Learned"
              value={stats.total}
              prefix={<BookOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={5}>
          <Card>
            <Statistic
              title="Strong"
              value={stats.strong}
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={5}>
          <Card>
            <Statistic
              title="Good"
              value={stats.good}
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={5}>
          <Card>
            <Statistic
              title="Fading"
              value={stats.fading}
              prefix={<WarningOutlined />}
              valueStyle={{ color: stats.fading > 0 ? '#fa8c16' : '#999' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={5}>
          <Card>
            <Statistic
              title="Critical"
              value={stats.critical}
              prefix={<WarningOutlined />}
              valueStyle={{ color: stats.critical > 0 ? '#f5222d' : '#999' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Filters */}
      <Card style={{ marginTop: 16 }}>
        <Space wrap size="middle" style={{ width: '100%' }}>
          <Input
            placeholder="Search concepts..."
            prefix={<SearchOutlined />}
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            style={{ width: isMobile ? '100%' : 200 }}
            allowClear
          />
          <Select
            value={statusFilter}
            onChange={setStatusFilter}
            style={{ width: 130 }}
            options={[
              { label: 'All Memory', value: 'all' },
              { label: 'Strong', value: 'strong' },
              { label: 'Good', value: 'good' },
              { label: 'Fading', value: 'fading' },
              { label: 'Critical', value: 'critical' },
            ]}
          />
          <Select
            value={stateFilter}
            onChange={setStateFilter}
            style={{ width: 140 }}
            options={[
              { label: 'All States', value: 'all' },
              { label: 'Learning', value: 'LEARNING' },
              { label: 'Review', value: 'REVIEW' },
              { label: 'Relearning', value: 'RELEARNING' },
            ]}
          />
          {topicGroups.length > 1 && (
            <Select
              value={topicFilter}
              onChange={setTopicFilter}
              style={{ width: 160 }}
              options={[
                { label: 'All Topics', value: 'all' },
                ...topicGroups.map((g) => ({ label: g, value: g })),
              ]}
            />
          )}
        </Space>
      </Card>

      {/* Table */}
      <Card style={{ marginTop: 16 }}>
        <Table<ReviewCard>
          dataSource={filteredCards}
          columns={columns}
          rowKey="concept_id"
          size={isMobile ? 'small' : 'middle'}
          pagination={filteredCards.length > 20 ? { pageSize: 20, showSizeChanger: true } : false}
          scroll={isMobile ? { x: 600 } : undefined}
        />
      </Card>
    </div>
  );
}

/* ── Main Page ── */
function ReviewQueue() {
  const { data: user } = useMe();
  const { data: reviewData, isLoading: reviewLoading } = useReviewQueue(user?.id);

  const summaryRef = useRef<HTMLDivElement>(null!);
  const dueRef = useRef<HTMLDivElement>(null!);
  const upcomingRef = useRef<HTMLDivElement>(null!);

  const dueNow = reviewData?.due_now || [];

  const tourSteps = [
    {
      title: 'Review Summary',
      description: '"Due Now" = concepts you should review today. "Critical" = memories fading fast and need immediate attention.',
      target: () => summaryRef.current!,
    },
    {
      title: 'Due for Review',
      description: 'These concepts need practice now. The circular indicator shows memory strength — red means it is fading quickly.',
      target: () => dueRef.current!,
    },
    {
      title: 'Upcoming Reviews',
      description: 'These reviews are coming up soon. The system schedules them at optimal intervals to maximize your retention.',
      target: () => upcomingRef.current!,
    },
  ];

  if (reviewLoading) {
    return <Spin size="large" className="center-spin" />;
  }

  const tabItems = [
    {
      key: 'queue',
      label: (
        <span>
          <ThunderboltOutlined />
          Review Queue
          {dueNow.length > 0 && (
            <Badge count={dueNow.length} size="small" offset={[8, -2]} />
          )}
        </span>
      ),
      children: (
        <ReviewQueueTab
          reviewData={reviewData}
          summaryRef={summaryRef}
          dueRef={dueRef}
          upcomingRef={upcomingRef}
        />
      ),
    },
    {
      key: 'all',
      label: (
        <span>
          <BookOutlined />
          All Concepts
        </span>
      ),
      children: <AllConceptsView userId={user?.id} />,
    },
  ];

  return (
    <div>
      <PageTour tourKey="reviewQueue" steps={tourSteps} />
      <Title level={3}>
        <CalendarOutlined style={{ marginRight: 8 }} />
        <TermTooltip term="review_queue">Review Queue</TermTooltip>
      </Title>

      <Tabs defaultActiveKey="queue" items={tabItems} />
    </div>
  );
}

export default ReviewQueue;
