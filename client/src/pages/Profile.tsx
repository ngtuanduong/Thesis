import { useMemo } from 'react';
import {
  Card,
  Typography,
  Descriptions,
  Spin,
  Progress,
  List,
  Tag,
  Row,
  Col,
  Statistic,
  Space,
} from 'antd';
import {
  TrophyOutlined,
  CheckCircleOutlined,
  BookOutlined,
  BulbOutlined,
} from '@ant-design/icons';
import { useMe } from '../api/queries/useAuth';
import { useKnowledgeState } from '../api/queries/useAdaptive';
import GuidedEmptyState from '../components/onboarding/GuidedEmptyState';
import TermTooltip from '../components/onboarding/TermTooltip';
import type { ConceptState } from '../types';

const { Title, Text } = Typography;

// Same status convention used by KnowledgeMap.tsx — keep colors consistent.
const statusConfig: Record<
  ConceptState['status'],
  { color: string; label: string; icon: React.ReactNode }
> = {
  mastered: {
    color: '#52c41a',
    label: 'Mastered',
    icon: <CheckCircleOutlined />,
  },
  learning: {
    color: '#1890ff',
    label: 'Learning',
    icon: <BookOutlined />,
  },
  not_started: {
    color: '#d9d9d9',
    label: 'Not Started',
    icon: <BulbOutlined />,
  },
};

const topicGroupLabels: Record<string, string> = {
  basics: 'Basics',
  control_flow: 'Control Flow',
  functions: 'Functions',
  data_structures: 'Data Structures',
  oop: 'Object-Oriented Programming',
  algorithms: 'Algorithms',
  advanced: 'Advanced',
};

function Profile() {
  const { data: user, isLoading: userLoading } = useMe();
  const { data: knowledgeState, isLoading: kstateLoading } = useKnowledgeState(
    user?.id,
  );

  // Group concepts by topic_group (sorted by difficulty_tier then name)
  const groupedConcepts = useMemo(() => {
    if (!knowledgeState?.concepts) return {};
    const groups: Record<string, ConceptState[]> = {};
    for (const c of knowledgeState.concepts) {
      const key = c.topic_group || 'other';
      if (!groups[key]) groups[key] = [];
      groups[key].push(c);
    }
    // Sort each group: by difficulty tier, then display name
    for (const list of Object.values(groups)) {
      list.sort((a, b) => {
        if (a.difficulty_tier !== b.difficulty_tier) {
          return a.difficulty_tier - b.difficulty_tier;
        }
        return a.display_name.localeCompare(b.display_name);
      });
    }
    return groups;
  }, [knowledgeState?.concepts]);

  if (userLoading) {
    return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />;
  }

  const summary = knowledgeState?.summary;

  return (
    <div>
      <Title level={3}>Profile</Title>

      <Card style={{ marginTop: 16 }}>
        <Descriptions column={1} bordered>
          <Descriptions.Item label="Name">{user?.name || 'N/A'}</Descriptions.Item>
          <Descriptions.Item label="Email">{user?.email || 'N/A'}</Descriptions.Item>
          <Descriptions.Item label="Role">{user?.role || 'N/A'}</Descriptions.Item>
        </Descriptions>
      </Card>

      <Card
        title={
          <span>
            <TrophyOutlined style={{ marginRight: 8 }} />
            Concept Mastery
          </span>
        }
        style={{ marginTop: 16 }}
      >
        {kstateLoading ? (
          <div style={{ textAlign: 'center', padding: 20 }}>
            <Spin />
          </div>
        ) : !knowledgeState || !knowledgeState.concepts?.length ? (
          <GuidedEmptyState type="knowledge" />
        ) : (
          <>
            {/* Summary row — overall stats from BKT */}
            {summary && (
              <Row gutter={16} style={{ marginBottom: 24 }}>
                <Col xs={12} sm={6}>
                  <Statistic
                    title="Mastered"
                    value={summary.mastered}
                    suffix={`/ ${summary.total_concepts}`}
                    valueStyle={{ color: statusConfig.mastered.color }}
                    prefix={statusConfig.mastered.icon}
                  />
                </Col>
                <Col xs={12} sm={6}>
                  <Statistic
                    title="Learning"
                    value={summary.learning}
                    valueStyle={{ color: statusConfig.learning.color }}
                    prefix={statusConfig.learning.icon}
                  />
                </Col>
                <Col xs={12} sm={6}>
                  <Statistic
                    title="Not Started"
                    value={summary.not_started}
                    valueStyle={{ color: '#8c8c8c' }}
                    prefix={statusConfig.not_started.icon}
                  />
                </Col>
                <Col xs={12} sm={6}>
                  <Statistic
                    title="Overall Mastery"
                    value={Math.round((summary.overall_mastery || 0) * 100)}
                    suffix="%"
                    valueStyle={{ color: '#1677ff' }}
                  />
                </Col>
              </Row>
            )}

            <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
              <TermTooltip term="mastery">Mastery</TermTooltip> is estimated using a
              probabilistic model updated after every submission. Percentages
              reflect the estimated probability that you have learned the
              concept, accounting for slips and guesses.
            </Text>

            {/* Concept list grouped by topic */}
            {Object.entries(groupedConcepts).map(([topic, concepts]) => (
              <div key={topic} style={{ marginBottom: 24 }}>
                <Title level={5} style={{ marginBottom: 8 }}>
                  {topicGroupLabels[topic] || topic}
                </Title>
                <List
                  dataSource={concepts}
                  renderItem={(c) => {
                    const percentage = Math.round(c.p_mastery * 100);
                    const cfg = statusConfig[c.status] || statusConfig.not_started;
                    return (
                      <List.Item>
                        <div style={{ width: '100%' }}>
                          <div
                            style={{
                              marginBottom: 6,
                              display: 'flex',
                              justifyContent: 'space-between',
                              alignItems: 'center',
                              flexWrap: 'wrap',
                              gap: 8,
                            }}
                          >
                            <Space size={8} wrap>
                              <Text strong>{c.display_name}</Text>
                              <Tag color={cfg.color} icon={cfg.icon}>
                                {cfg.label}
                              </Tag>
                              <Tag>Tier {c.difficulty_tier}</Tag>
                            </Space>
                            <Space size={12}>
                              <Text type="secondary" style={{ fontSize: 12 }}>
                                {c.n_correct}/{c.n_attempts} correct
                              </Text>
                              <Text strong style={{ color: cfg.color }}>
                                {percentage}%
                              </Text>
                            </Space>
                          </div>
                          <Progress
                            percent={percentage}
                            strokeColor={cfg.color}
                            showInfo={false}
                            size="small"
                          />
                        </div>
                      </List.Item>
                    );
                  }}
                />
              </div>
            ))}
          </>
        )}
      </Card>
    </div>
  );
}

export default Profile;
