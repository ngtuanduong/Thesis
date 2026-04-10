import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Table, Tag, Typography, Input, Space, Select } from 'antd';
import { SearchOutlined, FilterOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useProblemsPaginated } from '../api/queries/useProblems';
import { useConcepts } from '../api/queries/useAdaptive';
import { useResponsive } from '../hooks/useResponsive';

const { Title, Text } = Typography;

interface ProblemRow {
  id: string;
  title: string;
  description: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  problemConcepts?: { concept: { id: number; displayName: string }; isPrimary: boolean }[];
}

const difficultyColors: Record<string, string> = {
  EASY: 'green',
  MEDIUM: 'orange',
  HARD: 'red',
};

function Problems() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const initialSearch = params.get('search') || '';
  const initialConcept = params.get('concept') || '';

  const [searchText, setSearchText] = useState(initialSearch);
  const [debouncedSearch, setDebouncedSearch] = useState(initialSearch);
  const [selectedConcepts, setSelectedConcepts] = useState<number[]>(() => {
    if (initialConcept) return [Number(initialConcept)];
    return [];
  });
  const [selectedDifficulties, setSelectedDifficulties] = useState<string[]>([]);
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(15);

  const { isMobile } = useResponsive();
  const { data: allConcepts } = useConcepts();

  // Debounce search text
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchText);
      setPage(1);
    }, 300);
    return () => clearTimeout(timer);
  }, [searchText]);

  // Reset to page 1 when filters change
  useEffect(() => {
    setPage(1);
  }, [selectedDifficulties, selectedConcepts]);

  const { data, isLoading, isFetching } = useProblemsPaginated({
    page,
    pageSize,
    search: debouncedSearch || undefined,
    difficulty: selectedDifficulties.length ? selectedDifficulties : undefined,
    concepts: selectedConcepts.length ? selectedConcepts : undefined,
  });

  const hasActiveFilters = selectedConcepts.length > 0 || selectedDifficulties.length > 0;

  const clearAll = () => {
    setSearchText('');
    setDebouncedSearch('');
    setSelectedConcepts([]);
    setSelectedDifficulties([]);
  };

  const columns: ColumnsType<ProblemRow> = [
    {
      title: '#',
      key: 'index',
      width: 50,
      responsive: ['md'] as any,
      render: (_: unknown, __: ProblemRow, index: number) => (page - 1) * pageSize + index + 1,
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
    },
    {
      title: 'Concepts',
      key: 'concepts',
      width: 200,
      responsive: ['md'] as any,
      render: (_: unknown, record: ProblemRow) => {
        const concepts = record.problemConcepts;
        if (!concepts || concepts.length === 0) return <Text type="secondary">--</Text>;
        return (
          <Space size={[4, 4]} wrap>
            {concepts.map((pc, idx) => (
              <Tag
                key={idx}
                color={pc.isPrimary ? 'blue' : 'default'}
                style={{ cursor: 'pointer' }}
                onClick={(e) => {
                  e.stopPropagation();
                  if (!selectedConcepts.includes(pc.concept.id)) {
                    setSelectedConcepts((prev) => [...prev, pc.concept.id]);
                  }
                }}
              >
                {pc.concept.displayName}
              </Tag>
            ))}
          </Space>
        );
      },
    },
  ];

  return (
    <div>
      <div className="responsive-page-header">
        <Title level={3} style={{ margin: 0 }}>Problems</Title>
      </div>

      {/* Unified search & filter bar */}
      <div className="filter-bar" style={{ marginTop: 12 }}>
        <Input
          placeholder="Search by title..."
          prefix={<SearchOutlined />}
          style={{ width: isMobile ? '100%' : 220, flexShrink: 0 }}
          allowClear
          value={searchText}
          onChange={(e) => setSearchText(e.target.value)}
        />

        <Select
          mode="multiple"
          placeholder="Difficulty"
          style={{ minWidth: 140 }}
          maxTagCount="responsive"
          allowClear
          value={selectedDifficulties}
          onChange={setSelectedDifficulties}
          options={[
            { label: <Tag color="green">EASY</Tag>, value: 'EASY' },
            { label: <Tag color="orange">MEDIUM</Tag>, value: 'MEDIUM' },
            { label: <Tag color="red">HARD</Tag>, value: 'HARD' },
          ]}
        />

        <Select
          mode="multiple"
          placeholder="Concepts"
          style={{ minWidth: 160, flex: 1, maxWidth: 360 }}
          maxTagCount="responsive"
          allowClear
          showSearch
          value={selectedConcepts}
          onChange={setSelectedConcepts}
          options={(allConcepts ?? []).map((c) => ({ label: c.displayName, value: c.id }))}
          filterOption={(input, option) =>
            (option?.label as string)?.toLowerCase().includes(input.toLowerCase()) ?? false
          }
        />

        {hasActiveFilters && (
          <a onClick={clearAll} style={{ fontSize: 12, whiteSpace: 'nowrap' }}>
            <FilterOutlined /> Clear filters
          </a>
        )}
      </div>

      {/* Result count */}
      <div style={{ marginTop: 8, marginBottom: 4 }}>
        <Text type="secondary" style={{ fontSize: 12 }}>
          {data?.total ?? 0} problem{(data?.total ?? 0) !== 1 ? 's' : ''}
          {hasActiveFilters || debouncedSearch ? ' found' : ''}
        </Text>
      </div>

      <Table
        columns={columns}
        dataSource={data?.data}
        rowKey="id"
        loading={isLoading || isFetching}
        pagination={{
          current: page,
          pageSize,
          total: data?.total ?? 0,
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
        scroll={{ x: 500 }}
      />
    </div>
  );
}

export default Problems;
