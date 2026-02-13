import { useNavigate } from 'react-router-dom';
import { Table, Tag, Typography, Input, Space } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useProblems } from '../api/queries/useProblems';

const { Title } = Typography;

interface Problem {
  id: string;
  title: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  tags: string[];
}

const difficultyColors: Record<string, string> = {
  EASY: 'green',
  MEDIUM: 'orange',
  HARD: 'red',
};

function Problems() {
  const navigate = useNavigate();
  const { data: problems, isLoading } = useProblems();

  const columns: ColumnsType<Problem> = [
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      render: (text: string, record: Problem) => (
        <a onClick={() => navigate(`/problems/${record.id}`)}>{text}</a>
      ),
    },
    {
      title: 'Difficulty',
      dataIndex: 'difficulty',
      key: 'difficulty',
      width: 120,
      render: (difficulty: string) => (
        <Tag color={difficultyColors[difficulty]}>{difficulty}</Tag>
      ),
      filters: [
        { text: 'Easy', value: 'EASY' },
        { text: 'Medium', value: 'MEDIUM' },
        { text: 'Hard', value: 'HARD' },
      ],
      onFilter: (value, record) => record.difficulty === value,
    },
    {
      title: 'Tags',
      dataIndex: 'tags',
      key: 'tags',
      render: (tags: string[]) => (
        <Space size={[0, 4]} wrap>
          {tags?.map((tag) => <Tag key={tag}>{tag}</Tag>)}
        </Space>
      ),
    },
  ];

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Title level={3}>Problems</Title>
        <Input
          placeholder="Search problems..."
          prefix={<SearchOutlined />}
          style={{ width: 300 }}
        />
      </div>
      <Table
        columns={columns}
        dataSource={problems}
        rowKey="id"
        loading={isLoading}
        style={{ marginTop: 16 }}
      />
    </div>
  );
}

export default Problems;
