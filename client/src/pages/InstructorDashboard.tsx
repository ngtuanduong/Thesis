import { useState, useEffect } from 'react';
import {
  Card,
  Statistic,
  Progress,
  Table,
  Tag,
  Select,
  Row,
  Col,
  Typography,
  Button,
  Space,
  Input,
  Spin,
  Empty,
} from 'antd';
import type { ColumnsType } from 'antd/es/table';
import {
  TeamOutlined,
  FileTextOutlined,
  TrophyOutlined,
  WarningOutlined,
  SearchOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import {
  useInstructorDashboard,
  useInstructorProblems,
  useCourses,
} from '../api/queries/useInstructor';
import { useResponsive } from '../hooks/useResponsive';
import { sorterTooltip } from '../components/columnHelper';

const { Title, Text } = Typography;

const difficultyColors: Record<string, string> = {
  EASY: 'green',
  MEDIUM: 'orange',
  HARD: 'red',
};

interface StrugglingStudentRow {
  id: string;
  email: string;
  name: string;
  averageMastery: number;
}

interface ProblemConcept {
  id: number;
  name: string;
  displayName: string;
  isPrimary: boolean;
}

interface ProblemRow {
  id: string;
  title: string;
  description: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  courseId: string;
  createdAt: string;
  submissionCount: number;
  acceptedCount: number;
  acceptanceRate: number;
  testCaseCount: number;
  concepts: ProblemConcept[];
}

function InstructorDashboard() {
  const navigate = useNavigate();
  const { isMobile } = useResponsive();
  const { data: courses, isLoading: coursesLoading } = useCourses();
  const [selectedCourseId, setSelectedCourseId] = useState<string>('');
  const [problemSearch, setProblemSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [problemPage, setProblemPage] = useState(1);
  const [problemPageSize, setProblemPageSize] = useState(10);

  // Auto-select first course when courses load
  const activeCourseId = selectedCourseId || courses?.[0]?.id || '';

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(problemSearch);
      setProblemPage(1);
    }, 300);
    return () => clearTimeout(timer);
  }, [problemSearch]);

  const { data: dashboard, isLoading: dashboardLoading } =
    useInstructorDashboard(activeCourseId);
  const { data: problemsData, isLoading: problemsLoading, isFetching: problemsFetching } =
    useInstructorProblems({
      page: problemPage,
      pageSize: problemPageSize,
      search: debouncedSearch || undefined,
      courseId: activeCourseId || undefined,
    });

  const strugglingColumns: ColumnsType<StrugglingStudentRow> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (name: string) => <Text strong>{name}</Text>,
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
      responsive: ['md'] as any,
    },
    {
      title: 'Average Mastery',
      dataIndex: 'averageMastery',
      key: 'averageMastery',
      sorter: (a, b) => a.averageMastery - b.averageMastery,
      showSorterTooltip: sorterTooltip('Mean BKT mastery across all concepts. Click to sort.'),
      render: (val: number) => (
        <Progress
          percent={Math.round(val * 100)}
          size="small"
          status={val < 0.3 ? 'exception' : val < 0.6 ? 'normal' : 'success'}
        />
      ),
    },
  ];

  const problemColumns: ColumnsType<ProblemRow> = [
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      sorter: (a, b) => a.title.localeCompare(b.title),
      render: (title: string) => <Text strong>{title}</Text>,
    },
    {
      title: 'Difficulty',
      dataIndex: 'difficulty',
      key: 'difficulty',
      width: 110,
      render: (difficulty: string) => (
        <Tag color={difficultyColors[difficulty]}>{difficulty}</Tag>
      ),
    },
    {
      title: 'Concepts',
      dataIndex: 'concepts',
      key: 'concepts',
      width: 220,
      responsive: ['lg'] as any,
      render: (concepts: ProblemConcept[]) =>
        concepts && concepts.length > 0 ? (
          <Space size={[4, 4]} wrap>
            {concepts.map((c) => (
              <Tag key={c.id} color={c.isPrimary ? 'blue' : 'default'}>
                {c.displayName}
              </Tag>
            ))}
          </Space>
        ) : (
          <Text type="secondary">--</Text>
        ),
    },
    {
      title: 'Submissions',
      dataIndex: 'submissionCount',
      key: 'submissionCount',
      width: 110,
      responsive: ['md'] as any,
      sorter: (a, b) => a.submissionCount - b.submissionCount,
      showSorterTooltip: sorterTooltip('Total student submissions for this problem. Click to sort.'),
      align: 'right',
    },
    {
      title: 'Acceptance Rate',
      dataIndex: 'acceptanceRate',
      key: 'acceptanceRate',
      width: 150,
      responsive: ['md'] as any,
      sorter: (a, b) => a.acceptanceRate - b.acceptanceRate,
      showSorterTooltip: sorterTooltip('Percentage of submissions that pass all test cases. Click to sort.'),
      render: (rate: number) => (
        <Progress
          percent={Math.round(rate * 100)}
          size="small"
          strokeColor={rate >= 0.6 ? '#52c41a' : rate >= 0.3 ? '#faad14' : '#ff4d4f'}
        />
      ),
    },
    {
      title: 'Test Cases',
      dataIndex: 'testCaseCount',
      key: 'testCaseCount',
      width: 100,
      align: 'right',
      responsive: ['lg'] as any,
    },
  ];

  if (coursesLoading) {
    return (
      <div style={{ textAlign: 'center', padding: 80 }}>
        <Spin size="large" />
      </div>
    );
  }

  if (!courses || courses.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: 80 }}>
        <Empty description="No courses found. Create a course to get started." />
      </div>
    );
  }

  return (
    <div>
      {/* Header */}
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col xs={24} sm={10}>
          <Title level={3} style={{ margin: 0 }}>
            Instructor Dashboard
          </Title>
        </Col>
        <Col xs={24} sm={14}>
          <Space>
            <Text type="secondary">Course:</Text>
            <Select
              value={activeCourseId}
              onChange={(value) => setSelectedCourseId(value)}
              style={{ width: '100%' }}
              placeholder="Select a course"
            >
              {courses.map((course) => (
                <Select.Option key={course.id} value={course.id}>
                  {course.title}
                </Select.Option>
              ))}
            </Select>
          </Space>
        </Col>
      </Row>

      {/* Stats Row */}
      <Row gutter={[16, 16]}>
        <Col xs={12} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Enrolled Students"
              value={dashboard?.enrolledCount ?? 0}
              prefix={<TeamOutlined />}
              valueStyle={{ color: '#1890ff' }}
              loading={dashboardLoading}
            />
          </Card>
        </Col>
        <Col xs={12} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Submissions"
              value={dashboard?.totalSubmissions ?? 0}
              prefix={<FileTextOutlined />}
              loading={dashboardLoading}
            />
          </Card>
        </Col>
        <Col xs={12} sm={12} lg={6}>
          <Card>
            {dashboardLoading ? (
              <Spin />
            ) : (
              <div>
                <Text type="secondary" style={{ fontSize: 14 }}>
                  Average Mastery
                </Text>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 12,
                    marginTop: 8,
                  }}
                >
                  <Progress
                    type="circle"
                    percent={Math.round((dashboard?.averageMastery ?? 0) * 100)}
                    size={56}
                    strokeColor={{
                      '0%': '#108ee9',
                      '100%': '#87d068',
                    }}
                  />
                  <TrophyOutlined
                    style={{ fontSize: 20, color: '#faad14' }}
                  />
                </div>
              </div>
            )}
          </Card>
        </Col>
        <Col xs={12} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Struggling Students"
              value={dashboard?.strugglingStudents?.length ?? 0}
              prefix={<WarningOutlined />}
              valueStyle={{
                color:
                  (dashboard?.strugglingStudents?.length ?? 0) > 0
                    ? '#cf1322'
                    : '#3f8600',
              }}
              loading={dashboardLoading}
            />
          </Card>
        </Col>
      </Row>

      {/* Struggling Students Table */}
      <Card
        title="Struggling Students"
        style={{ marginTop: 24 }}
        extra={
          <Text type="secondary">
            Students with mastery below threshold
          </Text>
        }
      >
        {dashboardLoading ? (
          <div style={{ textAlign: 'center', padding: 40 }}>
            <Spin />
          </div>
        ) : !dashboard?.strugglingStudents ||
          dashboard.strugglingStudents.length === 0 ? (
          <Empty description="No struggling students. All students are performing well!" />
        ) : (
          <Table
            dataSource={dashboard.strugglingStudents}
            columns={strugglingColumns}
            rowKey="id"
            pagination={false}
            size="middle"
            scroll={{ x: 500 }}
          />
        )}
      </Card>

      {/* Problem Bank Table */}
      <Card
        title="Problem Bank"
        style={{ marginTop: 24 }}
        extra={
          <Space>
            <Input
              placeholder="Search problems..."
              prefix={<SearchOutlined />}
              value={problemSearch}
              onChange={(e) => setProblemSearch(e.target.value)}
              allowClear
              style={{ width: isMobile ? '100%' : 240 }}
            />
            <Button
              type="primary"
              icon={<SettingOutlined />}
              onClick={() => navigate('/instructor/problems')}
            >
              Manage Problems
            </Button>
          </Space>
        }
      >
        <Table
          dataSource={problemsData?.data}
          columns={problemColumns}
          rowKey="id"
          loading={problemsLoading || problemsFetching}
          pagination={{
            current: problemPage,
            pageSize: problemPageSize,
            total: problemsData?.total ?? 0,
            showSizeChanger: true,
            onChange: (p, s) => {
              if (s !== problemPageSize) {
                setProblemPageSize(s);
                setProblemPage(1);
              } else {
                setProblemPage(p);
              }
            },
          }}
          size="middle"
          locale={{ emptyText: <Empty description="No problems found" /> }}
          scroll={{ x: 500 }}
        />
      </Card>
    </div>
  );
}

export default InstructorDashboard;
