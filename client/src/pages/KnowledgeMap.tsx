import { useMemo } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  Handle,
  Position,
  MarkerType,
  type Node,
  type Edge,
  type NodeProps,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
// eslint-disable-next-line @typescript-eslint/no-require-imports
import Dagre from '@dagrejs/dagre';
import {
  Row,
  Col,
  Card,
  Typography,
  Progress,
  Spin,
  Empty,
  Tag,
  Statistic,
  Tooltip,
  Tabs,
  Table,
} from 'antd';
import {
  BulbOutlined,
  CheckCircleOutlined,
  BookOutlined,
  RocketOutlined,
  NodeIndexOutlined,
} from '@ant-design/icons';
import { useMe } from '../api/queries/useAuth';
import { useKnowledgeState } from '../api/queries/useAdaptive';
import type { ConceptState, KnowledgeGraphNode, KnowledgeGraphEdge } from '../types';

const { Title, Text } = Typography;

const topicColors: Record<string, string> = {
  basics: '#52c41a',
  control_flow: '#1890ff',
  functions: '#722ed1',
  data_structures: '#fa8c16',
  oop: '#eb2f96',
  algorithms: '#f5222d',
  advanced: '#13c2c2',
};

const topicLabels: Record<string, string> = {
  basics: 'Basics',
  control_flow: 'Control Flow',
  functions: 'Functions',
  data_structures: 'Data Structures',
  oop: 'OOP',
  algorithms: 'Algorithms',
  advanced: 'Advanced',
};

const statusConfig = {
  mastered: { color: '#52c41a', label: 'Mastered', icon: <CheckCircleOutlined /> },
  learning: { color: '#1890ff', label: 'Learning', icon: <BookOutlined /> },
  not_started: { color: '#d9d9d9', label: 'Not Started', icon: <BulbOutlined /> },
};

// ─── Custom ReactFlow Node ──────────────────────────────────────────────

type ConceptNodeData = {
  display_name: string;
  topic_group: string;
  difficulty_tier: number;
  p_mastery: number;
  status: string;
};

type ConceptNodeType = Node<ConceptNodeData, 'concept'>;

function ConceptNodeComponent({ data }: NodeProps<ConceptNodeType>) {
  const topicColor = topicColors[data.topic_group] || '#666';
  const statusCfg =
    statusConfig[data.status as keyof typeof statusConfig] || statusConfig.not_started;
  const pct = Math.round(data.p_mastery * 100);

  return (
    <>
      <Handle
        type="target"
        position={Position.Top}
        style={{ background: 'transparent', border: 'none' }}
      />
      <Tooltip
        title={
          <div>
            <div style={{ fontWeight: 600 }}>{data.display_name}</div>
            <div>Topic: {topicLabels[data.topic_group] || data.topic_group}</div>
            <div>Tier: {data.difficulty_tier}</div>
            <div>Mastery: {pct}%</div>
            <div>Status: {statusCfg.label}</div>
          </div>
        }
      >
        <div style={{ textAlign: 'center', cursor: 'default' }}>
          <div style={{ position: 'relative', width: 50, height: 50, margin: '0 auto' }}>
            {/* Outer ring — topic group color */}
            <div
              style={{
                position: 'absolute',
                inset: -3,
                borderRadius: '50%',
                border: `2.5px solid ${topicColor}`,
                opacity: 0.7,
              }}
            />
            {/* Inner circle — mastery fill */}
            <div
              style={{
                width: '100%',
                height: '100%',
                borderRadius: '50%',
                backgroundColor: statusCfg.color,
                opacity: 0.15 + data.p_mastery * 0.85,
                border: `2px solid ${statusCfg.color}`,
              }}
            />
            {/* Percentage overlay */}
            <div
              style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: 12,
                fontWeight: 600,
                color: data.p_mastery > 0.5 ? '#fff' : '#333',
              }}
            >
              {pct}%
            </div>
          </div>
          <div
            style={{
              fontSize: 10,
              color: '#555',
              marginTop: 4,
              maxWidth: 100,
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
            }}
          >
            {data.display_name}
          </div>
        </div>
      </Tooltip>
      <Handle
        type="source"
        position={Position.Bottom}
        style={{ background: 'transparent', border: 'none' }}
      />
    </>
  );
}

// Defined at module level to avoid re-renders (ReactFlow requirement)
const nodeTypes = { concept: ConceptNodeComponent };

// ─── Dagre Layout ───────────────────────────────────────────────────────

function buildGraphLayout(
  apiNodes: KnowledgeGraphNode[] | undefined,
  apiEdges: KnowledgeGraphEdge[] | undefined,
): { nodes: Node[]; edges: Edge[] } {
  if (!apiNodes?.length) return { nodes: [], edges: [] };
  const safeEdges = apiEdges ?? [];
  const nodeMap = new Map(apiNodes.map((n) => [n.id, n]));

  // 1. Run dagre to get optimal X ordering that minimizes edge crossings
  const g = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: 'TB', nodesep: 70, ranksep: 120 });

  apiNodes.forEach((n) => {
    g.setNode(String(n.id), { width: 110, height: 85 });
  });

  safeEdges.forEach((e) => {
    g.setEdge(String(e.from_id), String(e.to_id));
  });

  Dagre.layout(g);

  // 2. Constrain Y to tier bands but keep dagre's X ordering
  //    This preserves dagre's crossing-minimization while enforcing our tier structure
  const graphWidth = 1100;
  const tierGap = 140;

  const tierGroups = new Map<number, { id: number; dagreX: number }[]>();
  apiNodes.forEach((n) => {
    const pos = g.node(String(n.id));
    const list = tierGroups.get(n.difficulty_tier) || [];
    list.push({ id: n.id, dagreX: pos.x });
    tierGroups.set(n.difficulty_tier, list);
  });

  const sortedTiers = Array.from(tierGroups.keys()).sort((a, b) => a - b);
  const positions = new Map<number, { x: number; y: number }>();

  sortedTiers.forEach((tier, tierIdx) => {
    const group = tierGroups.get(tier)!;
    group.sort((a, b) => a.dagreX - b.dagreX);
    const gap = graphWidth / (group.length + 1);
    group.forEach((n, i) => {
      positions.set(n.id, {
        x: gap * (i + 1) - 55,
        y: tierIdx * tierGap,
      });
    });
  });

  // 3. Build ReactFlow nodes
  const rfNodes: Node[] = apiNodes.map((n) => ({
    id: String(n.id),
    type: 'concept' as const,
    position: positions.get(n.id) || { x: 0, y: 0 },
    data: {
      display_name: n.display_name,
      topic_group: n.topic_group,
      difficulty_tier: n.difficulty_tier,
      p_mastery: n.p_mastery,
      status: n.status,
    },
    draggable: false,
  }));

  // 4. Build ReactFlow edges
  const rfEdges: Edge[] = safeEdges.map((e) => {
    const from = nodeMap.get(e.from_id);
    const to = nodeMap.get(e.to_id);
    const isIntraTier = from && to && from.difficulty_tier === to.difficulty_tier;

    return {
      id: `e-${e.from_id}-${e.to_id}`,
      source: String(e.from_id),
      target: String(e.to_id),
      type: 'smoothstep',
      style: {
        stroke: isIntraTier ? '#ddd' : '#bbb',
        strokeWidth: isIntraTier ? 1 : 1.5,
        strokeDasharray: isIntraTier ? '4 3' : undefined,
      },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: isIntraTier ? '#ddd' : '#999',
        width: 15,
        height: 12,
      },
    };
  });

  return { nodes: rfNodes, edges: rfEdges };
}

// ─── Graph Visualization Component ──────────────────────────────────────

function KnowledgeGraphViz({
  nodes: graphNodes,
  edges: graphEdges,
}: {
  nodes: KnowledgeGraphNode[];
  edges: KnowledgeGraphEdge[];
}) {
  const { nodes, edges } = useMemo(
    () => buildGraphLayout(graphNodes, graphEdges),
    [graphNodes, graphEdges],
  );

  if (graphNodes.length === 0) {
    return <Empty description="No concepts found" />;
  }

  const tierCount = new Set(graphNodes.map((n) => n.difficulty_tier)).size;
  const graphHeight = Math.max(500, tierCount * 160 + 60);

  return (
    <div>
      <div
        style={{
          height: graphHeight,
          width: '100%',
          border: '1px solid #f0f0f0',
          borderRadius: 8,
        }}
      >
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          fitView
          fitViewOptions={{ padding: 0.15 }}
          nodesDraggable={false}
          nodesConnectable={false}
          elementsSelectable={false}
          minZoom={0.3}
          maxZoom={1.5}
        >
          <Background color="#f5f5f5" gap={20} />
          <Controls showInteractive={false} />
        </ReactFlow>
      </div>
      {/* Topic color legend */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: 16,
          marginTop: 12,
          justifyContent: 'center',
        }}
      >
        {Object.entries(topicColors).map(([key, color]) => (
          <div key={key} style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
            <div
              style={{
                width: 10,
                height: 10,
                borderRadius: '50%',
                backgroundColor: color,
                flexShrink: 0,
              }}
            />
            <Text type="secondary" style={{ fontSize: 12 }}>
              {topicLabels[key] || key}
            </Text>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─── Main Page Component ────────────────────────────────────────────────

function KnowledgeMap() {
  const { data: user } = useMe();
  const { data: knowledgeState, isLoading } = useKnowledgeState(user?.id);

  if (isLoading) {
    return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />;
  }

  if (!knowledgeState || knowledgeState.concepts.length === 0) {
    return (
      <div>
        <Title level={3}>
          <NodeIndexOutlined style={{ marginRight: 8 }} />
          Knowledge Map
        </Title>
        <Empty
          description="No knowledge data yet. Start solving problems to build your knowledge map!"
          style={{ marginTop: 60 }}
        />
      </div>
    );
  }

  const { concepts, knowledge_graph, summary } = knowledgeState;

  // Group concepts by topic
  const conceptsByTopic = concepts.reduce(
    (acc, c) => {
      const group = c.topic_group || 'other';
      if (!acc[group]) acc[group] = [];
      acc[group].push(c);
      return acc;
    },
    {} as Record<string, ConceptState[]>,
  );

  const columns = [
    {
      title: 'Concept',
      dataIndex: 'display_name',
      key: 'display_name',
      render: (text: string, record: ConceptState) => (
        <span>
          {text}
          <Tag
            color={topicColors[record.topic_group] || '#666'}
            style={{ marginLeft: 8 }}
          >
            Tier {record.difficulty_tier}
          </Tag>
        </span>
      ),
    },
    {
      title: 'Mastery',
      dataIndex: 'p_mastery',
      key: 'p_mastery',
      width: 200,
      sorter: (a: ConceptState, b: ConceptState) => a.p_mastery - b.p_mastery,
      render: (val: number) => {
        const pct = Math.round(val * 100);
        const color = pct >= 80 ? '#52c41a' : pct >= 50 ? '#1890ff' : '#faad14';
        return <Progress percent={pct} strokeColor={color} size="small" />;
      },
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      filters: [
        { text: 'Mastered', value: 'mastered' },
        { text: 'Learning', value: 'learning' },
        { text: 'Not Started', value: 'not_started' },
      ],
      onFilter: (value: any, record: ConceptState) => record.status === value,
      render: (status: string) => {
        const cfg = statusConfig[status as keyof typeof statusConfig] || statusConfig.not_started;
        return <Tag color={cfg.color}>{cfg.label}</Tag>;
      },
    },
    {
      title: 'Attempts',
      dataIndex: 'n_attempts',
      key: 'n_attempts',
      width: 90,
      sorter: (a: ConceptState, b: ConceptState) => a.n_attempts - b.n_attempts,
    },
    {
      title: 'Correct',
      dataIndex: 'n_correct',
      key: 'n_correct',
      width: 90,
      sorter: (a: ConceptState, b: ConceptState) => a.n_correct - b.n_correct,
    },
  ];

  return (
    <div>
      <Title level={3}>
        <NodeIndexOutlined style={{ marginRight: 8 }} />
        Knowledge Map
      </Title>

      {/* Summary Stats */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Overall Mastery"
              value={Math.round(summary.overall_mastery * 100)}
              suffix="%"
              valueStyle={{
                color: summary.overall_mastery >= 0.7 ? '#3f8600' : '#cf1322',
              }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Mastered"
              value={summary.mastered}
              suffix={`/ ${summary.total_concepts}`}
              prefix={<CheckCircleOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Learning"
              value={summary.learning}
              prefix={<BookOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="Not Started"
              value={summary.not_started}
              prefix={<RocketOutlined />}
              valueStyle={{ color: '#999' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Tabs for Graph and Table views */}
      <Card style={{ marginTop: 16 }}>
        <Tabs
          defaultActiveKey="graph"
          items={[
            {
              key: 'graph',
              label: 'Prerequisite Graph',
              children: (
                <KnowledgeGraphViz
                  nodes={knowledge_graph?.nodes ?? []}
                  edges={knowledge_graph?.edges ?? []}
                />
              ),
            },
            {
              key: 'topics',
              label: 'By Topic',
              children: (
                <Row gutter={[16, 16]}>
                  {Object.entries(conceptsByTopic).map(([topic, topicConcepts]) => {
                    const mastered = topicConcepts.filter(
                      (c) => c.status === 'mastered',
                    ).length;
                    const avgMastery =
                      topicConcepts.reduce((sum, c) => sum + c.p_mastery, 0) /
                      topicConcepts.length;

                    return (
                      <Col xs={24} sm={12} lg={8} key={topic}>
                        <Card
                          size="small"
                          title={
                            <span>
                              <Tag color={topicColors[topic] || '#666'}>
                                {topic.replace(/_/g, ' ').toUpperCase()}
                              </Tag>
                              <Text type="secondary" style={{ fontSize: 12 }}>
                                {mastered}/{topicConcepts.length} mastered
                              </Text>
                            </span>
                          }
                        >
                          {topicConcepts.map((c) => {
                            const pct = Math.round(c.p_mastery * 100);
                            const cfg =
                              statusConfig[c.status as keyof typeof statusConfig] ||
                              statusConfig.not_started;
                            return (
                              <div key={c.concept_id} style={{ marginBottom: 8 }}>
                                <div
                                  style={{
                                    display: 'flex',
                                    justifyContent: 'space-between',
                                    alignItems: 'center',
                                    marginBottom: 2,
                                  }}
                                >
                                  <Text style={{ fontSize: 13 }}>
                                    {c.display_name}
                                  </Text>
                                  <Tag
                                    color={cfg.color}
                                    style={{ fontSize: 10, lineHeight: '16px' }}
                                  >
                                    {pct}%
                                  </Tag>
                                </div>
                                <Progress
                                  percent={pct}
                                  strokeColor={cfg.color}
                                  size="small"
                                  showInfo={false}
                                />
                              </div>
                            );
                          })}
                          <div style={{ marginTop: 8, textAlign: 'right' }}>
                            <Text type="secondary" style={{ fontSize: 12 }}>
                              Avg: {(avgMastery * 100).toFixed(0)}%
                            </Text>
                          </div>
                        </Card>
                      </Col>
                    );
                  })}
                </Row>
              ),
            },
            {
              key: 'table',
              label: 'All Concepts',
              children: (
                <Table
                  dataSource={concepts}
                  columns={columns}
                  rowKey="concept_id"
                  size="small"
                  pagination={{ pageSize: 15 }}
                />
              ),
            },
          ]}
        />
      </Card>
    </div>
  );
}

export default KnowledgeMap;
