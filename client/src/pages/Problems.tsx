import { useState, useEffect, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Table, Tag, Typography, Input, Space, Select, Card, List, Spin, Collapse } from 'antd';
import { SearchOutlined, FilterOutlined, BulbOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useProblemsPaginated } from '../api/queries/useProblems';
import { useConcepts, useAdaptiveRecommendations } from '../api/queries/useAdaptive';
import { useMe } from '../api/queries/useAuth';
import { useResponsive } from '../hooks/useResponsive';
import PageTour from '../components/onboarding/PageTour';

const { Title } = Typography;

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

const { Text } = Typography;

function Problems() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const initialSearch = params.get('search') || '';
  const initialConcept = params.get('concept') || '';
  const { data: user } = useMe();
  const { data: recData, isLoading: recLoading } = useAdaptiveRecommendations(user?.id, 5);

  const recsRef = useRef<HTMLDivElement>(null);
  const filterBarRef = useRef<HTMLDivElement>(null);
  const tableRef = useRef<HTMLDivElement>(null);

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

  const tourSteps = [
    ...(recData?.recommendations?.length
      ? [
          {
            title: 'Recommended For You',
            description:
              'The adaptive engine analyzes your skill level, mastery, and review schedule to suggest problems that will help you learn most effectively.',
            target: () => recsRef.current!,
          },
        ]
      : []),
    {
      title: 'Search & Filter',
      description: 'Search problems by title, filter by difficulty level (Easy/Medium/Hard), or narrow down by specific concepts.',
      target: () => filterBarRef.current!,
    },
    {
      title: 'Problem List',
      description: 'Click any problem to start solving. Concept tags show which topics each problem covers — click a tag to filter by that concept.',
      target: () => tableRef.current!,
    },
  ];

  return (
    <div>
      <PageTour tourKey="problems" steps={tourSteps} />
      <div className="responsive-page-header">
        <Title level={3} style={{ margin: 0 }}>Problems</Title>
      </div>

      {/* Recommended For You */}
      {recLoading ? (
        <Card style={{ marginTop: 12, marginBottom: 12 }}>
          <div className="center-content"><Spin /></div>
        </Card>
      ) : recData?.recommendations && recData.recommendations.length > 0 ? (
        <div ref={recsRef}>
        <Collapse
          defaultActiveKey={['recs']}
          ghost
          style={{ marginTop: 12, marginBottom: 12 }}
          items={[{
            key: 'recs',
            label: (
              <span>
                <BulbOutlined style={{ color: '#fa8c16', marginRight: 8 }} />
                <Text strong>Recommended For You</Text>
                <Text type="secondary" style={{ marginLeft: 8, fontSize: 12 }}>
                  Powered by Adaptive Engine
                </Text>
              </span>
            ),
            children: (
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
            ),
          }]}
        />
        </div>
      ) : null}

      {/* Unified search & filter bar */}
      <div className="filter-bar" style={{ marginTop: 12 }} ref={filterBarRef}>
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

      <div ref={tableRef}>
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
    </div>
  );
}

export default Problems;
