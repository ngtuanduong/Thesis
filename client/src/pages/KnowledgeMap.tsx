import { useCallback, useMemo, useRef, useState } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  Panel,
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
  Popover,
  Tabs,
  Table,
} from 'antd';
import {
  BulbOutlined,
  CheckCircleOutlined,
  BookOutlined,
  RocketOutlined,
  NodeIndexOutlined,
  InfoCircleOutlined,
  CloseOutlined,
  ThunderboltOutlined,
  LoadingOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useMe } from '../api/queries/useAuth';
import { useKnowledgeState, usePracticeForConcept } from '../api/queries/useAdaptive';
import type { ConceptState, KnowledgeGraphNode, KnowledgeGraphEdge } from '../types';
import { useResponsive } from '../hooks/useResponsive';
import PageTour from '../components/onboarding/PageTour';
import TermTooltip from '../components/onboarding/TermTooltip';
import GuidedEmptyState from '../components/onboarding/GuidedEmptyState';
import styles from './KnowledgeMap.module.css';

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
  concept_id: number;
  concept_name: string;
  display_name: string;
  topic_group: string;
  difficulty_tier: number;
  p_mastery: number;
  status: string;
  _dimmed?: boolean;
  _selected?: boolean;
  _popoverOpen?: boolean;
};

type ConceptNodeType = Node<ConceptNodeData, 'concept'>;

function PracticeButton({ conceptId }: { conceptId: number }) {
  const navigate = useNavigate();
  const { data: user } = useMe();
  const practice = usePracticeForConcept();

  const handlePractice = () => {
    if (!user?.id) return;
    practice.mutate(
      { userId: user.id, conceptId },
      {
        onSuccess: (result) => {
          if (result.problem_id) {
            navigate(`/problems/${result.problem_id}`);
          } else {
            navigate(`/problems?concept=${conceptId}`);
          }
        },
        onError: () => {
          navigate(`/problems?concept=${conceptId}`);
        },
      },
    );
  };

  return (
    <div
      onClick={handlePractice}
      className={styles.popoverPractice}
      style={{ cursor: practice.isPending ? 'wait' : 'pointer' }}
    >
      {practice.isPending ? <LoadingOutlined /> : <ThunderboltOutlined />}
      {practice.isPending ? 'Loading...' : 'Practice'}
    </div>
  );
}

function ConceptNodeComponent({ data }: NodeProps<ConceptNodeType>) {
  const navigate = useNavigate();
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
      <Popover
        trigger={data._popoverOpen !== undefined ? [] : 'click'}
        open={data._popoverOpen !== undefined ? data._popoverOpen : undefined}
        content={
          <div className={styles.popoverContent}>
            <div className={styles.popoverTitle}>{data.display_name}</div>
            <div>Topic: {topicLabels[data.topic_group] || data.topic_group}</div>
            <div>Tier: {data.difficulty_tier}</div>
            <div>Mastery: {pct}%</div>
            <div>Status: {statusCfg.label}</div>
            <PracticeButton conceptId={data.concept_id} />
            <div
              onClick={() => navigate(`/problems?concept=${data.concept_id}`)}
              className={styles.popoverViewProblems}
            >
              <RocketOutlined /> View Problems
            </div>
          </div>
        }
      >
        <div className={styles.nodeCenter} style={{ opacity: data._dimmed ? 0.15 : 1 }}>
          <div className={styles.nodeRingContainer}>
            <div
              className={`${styles.nodeOuterRing}${data._selected ? ` ${styles.nodeSelected}` : ''}`}
              style={{ border: `2.5px solid ${topicColor}` }}
            />
            <div
              className={styles.nodeInnerCircle}
              style={{
                backgroundColor: statusCfg.color,
                opacity: 0.15 + data.p_mastery * 0.85,
                border: `2px solid ${statusCfg.color}`,
              }}
            />
            <div
              className={styles.nodePercentage}
              style={{ color: data.p_mastery > 0.5 ? '#fff' : '#333' }}
            >
              {pct}%
            </div>
          </div>
          <div className={styles.nodeLabel}>
            {data.display_name}
          </div>
        </div>
      </Popover>
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
  graphWidth = 1100,
  nodesep = 70,
  ranksep = 120,
): { nodes: Node[]; edges: Edge[] } {
  if (!apiNodes?.length) return { nodes: [], edges: [] };
  const safeEdges = apiEdges ?? [];
  const nodeMap = new Map(apiNodes.map((n) => [n.id, n]));

  // 1. Run dagre to get optimal X ordering that minimizes edge crossings
  const g = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: 'TB', nodesep: nodesep, ranksep: ranksep });

  apiNodes.forEach((n) => {
    g.setNode(String(n.id), { width: 110, height: 85 });
  });

  safeEdges.forEach((e) => {
    g.setEdge(String(e.from_id), String(e.to_id));
  });

  Dagre.layout(g);

  // 2. Constrain Y to tier bands but keep dagre's X ordering
  //    This preserves dagre's crossing-minimization while enforcing our tier structure
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
      concept_id: n.id,
      concept_name: n.name,
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
  graphWidth,
  nodesep,
  ranksep,
  isMobile,
  legendRef,
}: {
  nodes: KnowledgeGraphNode[];
  edges: KnowledgeGraphEdge[];
  graphWidth: number;
  nodesep: number;
  ranksep: number;
  isMobile: boolean;
  legendRef?: React.Ref<HTMLDivElement>;
}) {
  const [hoveredNodeId, setHoveredNodeId] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [popoverNodeId, setPopoverNodeId] = useState<string | null>(null);
  const [showHint, setShowHint] = useState(true);

  const activeNodeId = isMobile ? selectedNodeId : hoveredNodeId;

  const { nodes: baseNodes, edges: baseEdges } = useMemo(
    () => buildGraphLayout(graphNodes, graphEdges, graphWidth, nodesep, ranksep),
    [graphNodes, graphEdges, graphWidth, nodesep, ranksep],
  );

  // Pre-compute adjacency: for each node, which other nodes are its direct neighbors
  const adjacency = useMemo(() => {
    const neighbors = new Map<string, Set<string>>();
    for (const edge of baseEdges) {
      if (!neighbors.has(edge.source)) neighbors.set(edge.source, new Set());
      if (!neighbors.has(edge.target)) neighbors.set(edge.target, new Set());
      neighbors.get(edge.source)!.add(edge.target);
      neighbors.get(edge.target)!.add(edge.source);
    }
    return neighbors;
  }, [baseEdges]);

  // Apply dimming, selection, and popover state to nodes
  const displayNodes = useMemo(() => {
    if (!activeNodeId && !isMobile) return baseNodes;
    const connected = activeNodeId ? (adjacency.get(activeNodeId) || new Set()) : new Set();
    return baseNodes.map((n) => ({
      ...n,
      data: {
        ...n.data,
        _dimmed: activeNodeId ? (n.id !== activeNodeId && !connected.has(n.id)) : false,
        _selected: n.id === activeNodeId,
        ...(isMobile ? { _popoverOpen: n.id === popoverNodeId } : {}),
      },
    }));
  }, [baseNodes, activeNodeId, adjacency, isMobile, popoverNodeId]);

  // Edge visibility: hidden until a node is active (hover on desktop, tap on mobile)
  const displayEdges = useMemo(() => {
    if (!activeNodeId) {
      return baseEdges.map((e) => ({ ...e, hidden: true }));
    }
    return baseEdges.map((e) => {
      const isConnected = e.source === activeNodeId || e.target === activeNodeId;
      return {
        ...e,
        hidden: !isConnected,
        animated: isConnected,
        style: isConnected
          ? { stroke: '#1890ff', strokeWidth: 2 }
          : e.style,
        markerEnd: isConnected
          ? { type: MarkerType.ArrowClosed, color: '#1890ff', width: 15, height: 12 }
          : e.markerEnd,
      };
    });
  }, [baseEdges, activeNodeId]);

  const onNodeMouseEnter = useCallback((_: React.MouseEvent, node: Node) => {
    setHoveredNodeId(node.id);
  }, []);

  const onNodeMouseLeave = useCallback(() => {
    setHoveredNodeId(null);
  }, []);

  const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    if (!isMobile) return;
    setSelectedNodeId((prev) => {
      if (prev === node.id) {
        // Second tap on same node → open popover
        setPopoverNodeId(node.id);
        return prev;
      }
      // First tap on a node → select it (highlight edges), close any open popover
      setPopoverNodeId(null);
      return node.id;
    });
  }, [isMobile]);

  const onPaneClick = useCallback(() => {
    if (!isMobile) return;
    setSelectedNodeId(null);
    setPopoverNodeId(null);
  }, [isMobile]);

  if (graphNodes.length === 0) {
    return <Empty description="No concepts found" />;
  }

  const tierCount = new Set(graphNodes.map((n) => n.difficulty_tier)).size;
  const graphHeight = Math.max(500, tierCount * 160 + 60);

  return (
    <div>
      <div className={styles.graphContainer} style={{ height: graphHeight }}>
        <ReactFlow
          nodes={displayNodes}
          edges={displayEdges}
          nodeTypes={nodeTypes}
          onNodeMouseEnter={isMobile ? undefined : onNodeMouseEnter}
          onNodeMouseLeave={isMobile ? undefined : onNodeMouseLeave}
          onNodeClick={onNodeClick}
          onPaneClick={onPaneClick}
          fitView
          fitViewOptions={{ padding: isMobile ? 0.05 : 0.15 }}
          nodesDraggable={false}
          nodesConnectable={false}
          elementsSelectable={false}
          minZoom={0.3}
          maxZoom={1.5}
        >
          <Background color="#f5f5f5" gap={20} />
          <Controls showInteractive={false} />
          <Panel position="top-left">
            {showHint ? (
              <div className={styles.guidanceCard}>
                <CloseOutlined
                  onClick={() => setShowHint(false)}
                  className={styles.guidanceClose}
                />
                <div style={{ marginBottom: 4 }}>
                  <InfoCircleOutlined style={{ marginRight: 4, color: '#1890ff' }} />
                  <strong>Guidance</strong>
                </div>
                <div><strong>{isMobile ? 'Tap' : 'Hover'}</strong> {isMobile ? 'a node' : 'over a node'} to see related topics</div>
                <div><strong>{isMobile ? 'Tap again' : 'Click'}</strong> {isMobile ? 'to open details' : 'on a node to view details'}</div>
              </div>
            ) : (
              <div onClick={() => setShowHint(true)} className={styles.guidanceToggle}>
                <InfoCircleOutlined style={{ fontSize: 14, color: '#1890ff' }} />
              </div>
            )}
          </Panel>
        </ReactFlow>
      </div>
      {/* Topic color legend */}
      <div className={styles.legend} ref={legendRef}>
        {Object.entries(topicColors).map(([key, color]) => (
          <div key={key} className={styles.legendItem}>
            <div className={styles.legendDot} style={{ backgroundColor: color }} />
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
  const { isMobile, isTablet } = useResponsive();

  if (isLoading) {
    return <Spin size="large" className="center-spin" />;
  }

  if (!knowledgeState || knowledgeState.concepts.length === 0) {
    return (
      <div>
        <Title level={3}>
          <NodeIndexOutlined style={{ marginRight: 8 }} />
          Knowledge Map
        </Title>
        <GuidedEmptyState type="knowledge" />
      </div>
    );
  }

  const summaryRef = useRef<HTMLDivElement>(null);
  const graphRef = useRef<HTMLDivElement>(null);
  const legendRef = useRef<HTMLDivElement>(null);
  const tabsRef = useRef<HTMLDivElement>(null);

  const tourSteps = [
    {
      title: 'Mastery Overview',
      description: 'Your overall mastery at a glance. "Mastered" means the system is confident you truly understand this concept.',
      target: () => summaryRef.current!,
    },
    {
      title: 'Concept Graph',
      description: 'Each circle is a concept. Color = topic group, fill intensity = mastery level. Hover to see connections (prerequisites).',
      target: () => graphRef.current!,
    },
    {
      title: 'Topic Legend',
      description: 'Colors represent different topic groups. Click a node to see details and practice that concept.',
      target: () => legendRef.current!,
    },
    {
      title: 'View Options',
      description: 'Switch between the graph view, topic groups, or a sortable table of all concepts.',
      target: () => tabsRef.current!,
    },
  ];

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
      responsive: ['md'] as any,
      sorter: (a: ConceptState, b: ConceptState) => a.n_attempts - b.n_attempts,
    },
    {
      title: 'Correct',
      dataIndex: 'n_correct',
      key: 'n_correct',
      width: 90,
      responsive: ['md'] as any,
      sorter: (a: ConceptState, b: ConceptState) => a.n_correct - b.n_correct,
    },
  ];

  return (
    <div>
      <PageTour tourKey="knowledgeMap" steps={tourSteps} />
      <Title level={3}>
        <NodeIndexOutlined style={{ marginRight: 8 }} />
        Knowledge Map
      </Title>

      {/* Summary Stats */}
      <Row gutter={[16, 16]} style={{ marginTop: 16 }} ref={summaryRef}>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title={<TermTooltip term="mastery">Overall Mastery</TermTooltip>}
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
      <Card style={{ marginTop: 16 }} ref={tabsRef}>
        <Tabs
          defaultActiveKey="graph"
          items={[
            {
              key: 'graph',
              label: 'Prerequisite Graph',
              children: (
                <div ref={graphRef}>
                  <KnowledgeGraphViz
                    nodes={knowledge_graph?.nodes ?? []}
                    edges={knowledge_graph?.edges ?? []}
                    isMobile={isMobile}
                    graphWidth={isMobile ? 650 : isTablet ? 700 : 1100}
                    nodesep={isMobile ? 30 : 70}
                    ranksep={isMobile ? 80 : 120}
                    legendRef={legendRef}
                  />
                </div>
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
                              <div key={c.concept_id} className={styles.conceptRow}>
                                <div className={styles.conceptRowHeader}>
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
                          <div className={styles.topicFooter}>
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
