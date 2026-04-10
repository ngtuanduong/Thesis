import { useState, useEffect } from 'react';
import {
  Row,
  Col,
  Card,
  Statistic,
  Table,
  Tag,
  Select,
  Typography,
  Button,
  Space,
  Input,
  message,
  Popconfirm,
} from 'antd';
import {
  UserOutlined,
  FileOutlined,
  CodeOutlined,
  BookOutlined,
  ThunderboltOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import {
  useAdminStats,
  useAdminUsers,
  useAssignGroup,
  useExperimentStats,
} from '../api/queries/useAdmin';
import { useResponsive } from '../hooks/useResponsive';

const { Title, Text } = Typography;
const { Search } = Input;

interface AdminUser {
  id: string;
  email: string;
  name: string;
  role: string;
  createdAt: string;
  _count: { submissions: number };
  experimentGroup: { groupName: string; assignedAt: string } | null;
}

const roleColors: Record<string, string> = {
  ADMIN: 'red',
  INSTRUCTOR: 'blue',
  STUDENT: 'green',
};

const groupOptions = [
  { label: 'Experimental', value: 'experimental' },
  { label: 'Control', value: 'control' },
];

function AdminDashboard() {
  const { isMobile } = useResponsive();
  const [searchText, setSearchText] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [roleFilter, setRoleFilter] = useState<string[]>([]);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [pendingGroup, setPendingGroup] = useState<Record<string, string>>({});

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchText);
      setPage(1);
    }, 300);
    return () => clearTimeout(timer);
  }, [searchText]);

  // Reset page on filter change
  useEffect(() => {
    setPage(1);
  }, [roleFilter]);

  const { data: stats, isLoading: statsLoading } = useAdminStats();
  const { data: usersData, isLoading: usersLoading, isFetching } = useAdminUsers({
    page,
    pageSize,
    search: debouncedSearch || undefined,
    role: roleFilter.length ? roleFilter : undefined,
  });
  const { data: experimentStats } = useExperimentStats();
  const assignGroup = useAssignGroup();

  const handleAssignGroup = (userId: string) => {
    const groupName = pendingGroup[userId];
    if (!groupName) {
      message.warning('Please select a group first.');
      return;
    }
    assignGroup.mutate(
      { userId, groupName },
      {
        onSuccess: () => {
          message.success('Group assigned successfully.');
          setPendingGroup((prev) => {
            const next = { ...prev };
            delete next[userId];
            return next;
          });
        },
        onError: () => {
          message.error('Failed to assign group.');
        },
      },
    );
  };

  const columns: ColumnsType<AdminUser> = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: (a, b) => (a.name || '').localeCompare(b.name || ''),
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
      responsive: ['md'] as any,
    },
    {
      title: 'Role',
      dataIndex: 'role',
      key: 'role',
      width: 120,
      render: (role: string) => (
        <Tag color={roleColors[role] || 'default'}>{role}</Tag>
      ),
    },
    {
      title: 'Submissions',
      key: 'submissions',
      width: 120,
      align: 'center',
      responsive: ['lg'] as any,
      render: (_: unknown, record: AdminUser) => record._count?.submissions ?? 0,
      sorter: (a, b) => (a._count?.submissions ?? 0) - (b._count?.submissions ?? 0),
    },
    {
      title: 'Experiment Group',
      key: 'experimentGroup',
      width: 200,
      responsive: ['md'] as any,
      render: (_: unknown, record: AdminUser) =>
        record.experimentGroup ? (
          <Tag color="purple">{record.experimentGroup.groupName}</Tag>
        ) : (
          <Tag>Unassigned</Tag>
        ),
    },
    {
      title: 'Joined',
      dataIndex: 'createdAt',
      key: 'createdAt',
      width: 120,
      responsive: ['lg'] as any,
      render: (date: string) => new Date(date).toLocaleDateString(),
      sorter: (a, b) =>
        new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime(),
    },
    {
      title: 'Assign Group',
      key: 'action',
      width: 260,
      responsive: ['md'] as any,
      render: (_: unknown, record: AdminUser) => (
        <Space>
          <Select
            placeholder="Select group"
            options={groupOptions}
            value={pendingGroup[record.id] || undefined}
            onChange={(value) =>
              setPendingGroup((prev) => ({ ...prev, [record.id]: value }))
            }
            style={{ width: 140 }}
            size="small"
          />
          <Popconfirm
            title="Assign experiment group"
            description={`Assign "${pendingGroup[record.id] || '...'}" to ${record.name}?`}
            onConfirm={() => handleAssignGroup(record.id)}
            okText="Assign"
            disabled={!pendingGroup[record.id]}
          >
            <Button
              type="primary"
              size="small"
              disabled={!pendingGroup[record.id]}
              loading={assignGroup.isPending}
            >
              Assign
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={3}>Admin Dashboard</Title>

      {/* Platform Stats */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} sm={12} lg={4}>
          <Card>
            <Statistic
              title="Total Users"
              value={stats?.totalUsers ?? 0}
              prefix={<UserOutlined />}
              loading={statsLoading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={5}>
          <Card>
            <Statistic
              title="Total Submissions"
              value={stats?.totalSubmissions ?? 0}
              prefix={<FileOutlined />}
              loading={statsLoading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={5}>
          <Card>
            <Statistic
              title="Total Problems"
              value={stats?.totalProblems ?? 0}
              prefix={<CodeOutlined />}
              loading={statsLoading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={5}>
          <Card>
            <Statistic
              title="Total Courses"
              value={stats?.totalCourses ?? 0}
              prefix={<BookOutlined />}
              loading={statsLoading}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={5}>
          <Card>
            <Statistic
              title="Active Today"
              value={stats?.activeUsersToday ?? 0}
              prefix={<ThunderboltOutlined />}
              valueStyle={{ color: '#3f8600' }}
              loading={statsLoading}
            />
          </Card>
        </Col>
      </Row>

      {/* User Management */}
      <Card title="User Management" style={{ marginTop: 24 }}>
        <div style={{ marginBottom: 16, display: 'flex', flexWrap: 'wrap', gap: 8 }}>
          <Search
            placeholder="Search by name or email..."
            allowClear
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            style={{ width: isMobile ? '100%' : 280 }}
          />
          <Select
            mode="multiple"
            placeholder="Filter by role"
            allowClear
            value={roleFilter}
            onChange={setRoleFilter}
            style={{ minWidth: 180 }}
            options={[
              { label: <Tag color="red">ADMIN</Tag>, value: 'ADMIN' },
              { label: <Tag color="blue">INSTRUCTOR</Tag>, value: 'INSTRUCTOR' },
              { label: <Tag color="green">STUDENT</Tag>, value: 'STUDENT' },
            ]}
          />
        </div>
        <Table
          columns={columns}
          dataSource={usersData?.data}
          rowKey="id"
          loading={usersLoading || isFetching}
          pagination={{
            current: page,
            pageSize,
            total: usersData?.total ?? 0,
            showSizeChanger: true,
            onChange: (p, s) => {
              if (s !== pageSize) {
                setPageSize(s);
                setPage(1);
              } else {
                setPage(p);
              }
            },
          }}
          scroll={{ x: 900 }}
        />
      </Card>

      {/* Experiment Overview */}
      <Card title="Experiment Overview" style={{ marginTop: 24 }}>
        {experimentStats ? (
          <Row gutter={[16, 16]}>
            {experimentStats.groups?.map(
              (group: { groupName: string; count: number }) => (
                <Col xs={24} sm={8} key={group.groupName}>
                  <Card>
                    <Statistic
                      title={
                        <span>
                          <Tag color="purple">{group.groupName}</Tag> Group
                        </span>
                      }
                      value={group.count}
                      suffix="users"
                    />
                  </Card>
                </Col>
              ),
            )}
            <Col xs={24} sm={8}>
              <Card>
                <Statistic
                  title="Unassigned"
                  value={experimentStats.totalUnassigned ?? 0}
                  suffix="users"
                  valueStyle={{ color: '#999' }}
                />
              </Card>
            </Col>
          </Row>
        ) : (
          <Text type="secondary">
            No experiment data available yet.
          </Text>
        )}
      </Card>
    </div>
  );
}

export default AdminDashboard;
