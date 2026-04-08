import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Table, Tag, Typography, Input, Space } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useProblems } from '../api/queries/useProblems';

const { Title, Text } = Typography;

interface ProblemRow {
  id: string;
  title: string;
  description: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  tags: string[];
  problemConcepts?: { concept: { id: number; displayName: string }; isPrimary: boolean }[];
}

const difficultyColors: Record<string, string> = {
  EASY: 'green',
  MEDIUM: 'orange',
  HARD: 'red',
};

function Problems() {
  const navigate = useNavigate();
  const [searchText, setSearchText] = useState('');
  const { data: problems, isLoading } = useProblems();

  const filteredProblems = useMemo(() => {
    if (!problems) return [];
    let result = problems;

    // Search filter
    if (searchText) {
      const lower = searchText.toLowerCase();
      result = result.filter(
        (p: ProblemRow) =>
          p.title.toLowerCase().includes(lower) ||
          p.tags?.some((t) => t.toLowerCase().includes(lower)),
      );
    }

    return result;
  }, [problems, searchText]);

  const columns: ColumnsType<ProblemRow> = [
    {
      title: '#',
      key: 'index',
      width: 50,
      render: (_: unknown, __: ProblemRow, index: number) => index + 1,
    },
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      sorter: (a, b) => a.title.localeCompare(b.title),
      render: (text: string, record: ProblemRow) => (
        <a onClick={() => navigate(`/problems/${record.id}`)}>
          {text}
        </a>
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
      title: 'Concepts',
      key: 'concepts',
      width: 200,
      render: (_: unknown, record: ProblemRow) => {
        const concepts = record.problemConcepts;
        if (!concepts || concepts.length === 0) return <Text type="secondary">--</Text>;
        return (
          <Space size={[4, 4]} wrap>
            {concepts.map((pc, idx) => (
              <Tag key={idx} color={pc.isPrimary ? 'blue' : 'default'}>
                {pc.concept.displayName}
              </Tag>
            ))}
          </Space>
        );
      },
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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
        <Title level={3} style={{ margin: 0 }}>Problems</Title>
        <Space>
          <Input
            placeholder="Search by title or tag..."
            prefix={<SearchOutlined />}
            style={{ width: 280 }}
            allowClear
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />
        </Space>
      </div>
      <Table
        columns={columns}
        dataSource={filteredProblems}
        rowKey="id"
        loading={isLoading}
        style={{ marginTop: 16 }}
        pagination={{ pageSize: 15, showSizeChanger: true }}
      />
    </div>
  );
}

export default Problems;
