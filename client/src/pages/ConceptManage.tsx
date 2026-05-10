import { useState, useMemo, useCallback } from 'react';
import {
  Table,
  Modal,
  Form,
  Input,
  Select,
  Button,
  Tag,
  Popconfirm,
  Space,
  Typography,
  Card,
  message,
  Row,
  Col,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  SearchOutlined,
  ArrowRightOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { Concept } from '../types';
import {
  useConcepts,
  useKnowledgeGraph,
  useCreateConcept,
  useUpdateConcept,
  useDeleteConcept,
  useCreateEdge,
  useDeleteEdge,
} from '../api/queries/useConceptManage';
import { useResponsive } from '../hooks/useResponsive';

const { Title, Text } = Typography;

const TOPIC_GROUPS = [
  { label: 'Basics', value: 'basics' },
  { label: 'Control Flow', value: 'control_flow' },
  { label: 'Functions', value: 'functions' },
  { label: 'Data Structures', value: 'data_structures' },
  { label: 'OOP', value: 'oop' },
  { label: 'Algorithms', value: 'algorithms' },
  { label: 'Advanced', value: 'advanced' },
];

const TIER_OPTIONS = [
  { label: 'Tier 1 — Foundation', value: 1 },
  { label: 'Tier 2 — Core', value: 2 },
  { label: 'Tier 3 — Intermediate', value: 3 },
  { label: 'Tier 4 — Advanced', value: 4 },
  { label: 'Tier 5 — Expert', value: 5 },
];

const topicColors: Record<string, string> = {
  basics: 'green',
  control_flow: 'blue',
  functions: 'purple',
  data_structures: 'orange',
  oop: 'magenta',
  algorithms: 'red',
  advanced: 'cyan',
};

interface ConceptFormValues {
  name: string;
  displayName: string;
  description?: string;
  topicGroup: string;
  difficultyTier: number;
}

interface EdgeFormValues {
  fromConceptId: number;
  toConceptId: number;
}

function ConceptManage() {
  const [conceptForm] = Form.useForm<ConceptFormValues>();
  const [edgeForm] = Form.useForm<EdgeFormValues>();
  const [conceptModalOpen, setConceptModalOpen] = useState(false);
  const [edgeModalOpen, setEdgeModalOpen] = useState(false);
  const [editingConcept, setEditingConcept] = useState<Concept | null>(null);
  const [searchText, setSearchText] = useState('');
  const [edgeSearch, setEdgeSearch] = useState('');
  const { isMobile } = useResponsive();

  const { data: concepts, isLoading } = useConcepts();
  const { data: graphData } = useKnowledgeGraph();
  const createConcept = useCreateConcept();
  const updateConcept = useUpdateConcept();
  const deleteConcept = useDeleteConcept();
  const createEdge = useCreateEdge();
  const deleteEdge = useDeleteEdge();

  const filteredConcepts = useMemo(() => {
    if (!concepts) return [];
    if (!searchText) return concepts;
    const lower = searchText.toLowerCase();
    return concepts.filter(
      (c) =>
        c.displayName.toLowerCase().includes(lower) ||
        c.name.toLowerCase().includes(lower),
    );
  }, [concepts, searchText]);

  // Build a map from concept ID to displayName for edge display
  const conceptMap = useMemo(() => {
    const map = new Map<number, string>();
    for (const c of concepts ?? []) map.set(c.id, c.displayName);
    return map;
  }, [concepts]);

  // Filtered edges for search
  const filteredEdges = useMemo(() => {
    if (!graphData?.edges) return [];
    if (!edgeSearch) return graphData.edges;
    const lower = edgeSearch.toLowerCase();
    return graphData.edges.filter((e: any) => {
      const fromName = conceptMap.get(e.fromConceptId) || '';
      const toName = conceptMap.get(e.toConceptId) || '';
      return fromName.toLowerCase().includes(lower) || toName.toLowerCase().includes(lower);
    });
  }, [graphData?.edges, edgeSearch, conceptMap]);

  // ─── Concept CRUD ───
  const openCreateConcept = useCallback(() => {
    setEditingConcept(null);
    conceptForm.resetFields();
    conceptForm.setFieldsValue({ difficultyTier: 1, topicGroup: 'basics' });
    setConceptModalOpen(true);
  }, [conceptForm]);

  const openEditConcept = useCallback(
    (concept: Concept) => {
      setEditingConcept(concept);
      conceptForm.setFieldsValue({
        name: concept.name,
        displayName: concept.displayName,
        description: concept.description ?? '',
        topicGroup: concept.topicGroup ?? 'basics',
        difficultyTier: concept.difficultyTier,
      });
      setConceptModalOpen(true);
    },
    [conceptForm],
  );

  const closeConceptModal = useCallback(() => {
    setConceptModalOpen(false);
    setEditingConcept(null);
    conceptForm.resetFields();
  }, [conceptForm]);

  const handleConceptSubmit = useCallback(async () => {
    try {
      const values = await conceptForm.validateFields();
      if (editingConcept) {
        await updateConcept.mutateAsync({ id: editingConcept.id, ...values });
        message.success('Concept updated');
      } else {
        await createConcept.mutateAsync(values);
        message.success('Concept created');
      }
      closeConceptModal();
    } catch (err: any) {
      if (err?.errorFields) return;
      message.error(err?.response?.data?.message || 'Failed to save concept');
    }
  }, [conceptForm, editingConcept, createConcept, updateConcept, closeConceptModal]);

  const handleDeleteConcept = useCallback(
    async (id: number) => {
      try {
        await deleteConcept.mutateAsync(id);
        message.success('Concept deleted');
      } catch (err: any) {
        message.error(err?.response?.data?.message || 'Failed to delete concept');
      }
    },
    [deleteConcept],
  );

  // ─── Edge CRUD ───
  const openCreateEdge = useCallback(() => {
    edgeForm.resetFields();
    setEdgeModalOpen(true);
  }, [edgeForm]);

  const handleEdgeSubmit = useCallback(async () => {
    try {
      const values = await edgeForm.validateFields();
      await createEdge.mutateAsync(values);
      message.success('Prerequisite edge created');
      setEdgeModalOpen(false);
      edgeForm.resetFields();
    } catch (err: any) {
      if (err?.errorFields) return;
      message.error(err?.response?.data?.message || 'Failed to create edge');
    }
  }, [edgeForm, createEdge]);

  const handleDeleteEdge = useCallback(
    async (id: number) => {
      try {
        await deleteEdge.mutateAsync(id);
        message.success('Edge deleted');
      } catch {
        message.error('Failed to delete edge');
      }
    },
    [deleteEdge],
  );

  // ─── Columns ───
  const columns: ColumnsType<Concept> = [
    {
      title: 'Name',
      dataIndex: 'displayName',
      key: 'displayName',
      sorter: (a, b) => a.displayName.localeCompare(b.displayName),
      render: (text: string, record: Concept) => (
        <div>
          <Text strong>{text}</Text>
          <br />
          <Text type="secondary" style={{ fontSize: 12 }}>{record.name}</Text>
        </div>
      ),
    },
    {
      title: 'Topic',
      dataIndex: 'topicGroup',
      key: 'topicGroup',
      width: 140,
      responsive: ['md'] as any,
      filters: TOPIC_GROUPS.map((g) => ({ text: g.label, value: g.value })),
      onFilter: (value, record) => record.topicGroup === value,
      render: (group: string) => (
        <Tag color={topicColors[group] || 'default'}>
          {TOPIC_GROUPS.find((g) => g.value === group)?.label || group}
        </Tag>
      ),
    },
    {
      title: 'Tier',
      dataIndex: 'difficultyTier',
      key: 'difficultyTier',
      width: 80,
      sorter: (a, b) => a.difficultyTier - b.difficultyTier,
      render: (tier: number) => <Tag>{tier}</Tag>,
    },
    {
      title: 'Problems',
      key: 'problems',
      width: 90,
      responsive: ['md'] as any,
      render: (_: unknown, record: Concept) => record.problemConcepts?.length ?? 0,
      sorter: (a, b) => (a.problemConcepts?.length ?? 0) - (b.problemConcepts?.length ?? 0),
    },
    {
      title: 'Actions',
      key: 'actions',
      width: isMobile ? 80 : 150,
      render: (_: unknown, record: Concept) => (
        <Space size={isMobile ? 0 : 'small'}>
          <Button type="link" icon={<EditOutlined />} onClick={() => openEditConcept(record)}>
            {!isMobile && 'Edit'}
          </Button>
          <Popconfirm
            title="Delete concept?"
            description="This will also remove all prerequisite edges for this concept."
            onConfirm={() => handleDeleteConcept(record.id)}
            okText="Yes"
            cancelText="No"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              {!isMobile && 'Delete'}
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      {/* Header */}
      <div className="responsive-page-header">
        <Title level={3} style={{ margin: 0 }}>Concept Management</Title>
        <Space>
          <Input
            placeholder="Search concepts..."
            prefix={<SearchOutlined />}
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            style={{ width: isMobile ? '100%' : 220 }}
            allowClear
          />
          <Button type="primary" icon={<PlusOutlined />} onClick={openCreateConcept}>
            {isMobile ? 'Add' : 'Create Concept'}
          </Button>
        </Space>
      </div>

      {/* Concepts Table */}
      <Table
        columns={columns}
        dataSource={filteredConcepts}
        rowKey="id"
        loading={isLoading}
        pagination={{ pageSize: 15, showSizeChanger: false }}
        scroll={{ x: 500 }}
        size="middle"
      />

      {/* Prerequisite Edges Card */}
      <Card style={{ marginTop: 24 }}>
        <div className="responsive-page-header" style={{ marginBottom: 12 }}>
          <Title level={5} style={{ margin: 0 }}>
            Prerequisite Edges ({graphData?.edges?.length ?? 0})
          </Title>
          <Space>
            <Input
              placeholder="Search edges..."
              prefix={<SearchOutlined />}
              value={edgeSearch}
              onChange={(e) => setEdgeSearch(e.target.value)}
              allowClear
              style={{ width: isMobile ? '100%' : 200 }}
            />
            <Button icon={<PlusOutlined />} onClick={openCreateEdge}>
              {isMobile ? 'Add' : 'Add Edge'}
            </Button>
          </Space>
        </div>
        <Table
          size="small"
          dataSource={filteredEdges}
          rowKey="id"
          pagination={{ pageSize: 10, showSizeChanger: false }}
          scroll={{ x: 400 }}
          columns={[
            {
              title: 'Prerequisite',
              dataIndex: 'fromConceptId',
              key: 'from',
              render: (id: number) => <Tag color="blue">{conceptMap.get(id) || id}</Tag>,
            },
            {
              title: '',
              key: 'arrow',
              width: 40,
              render: () => <ArrowRightOutlined style={{ color: '#999' }} />,
            },
            {
              title: 'Dependent',
              dataIndex: 'toConceptId',
              key: 'to',
              render: (id: number) => <Tag>{conceptMap.get(id) || id}</Tag>,
            },
            {
              title: '',
              key: 'action',
              width: 50,
              render: (_: unknown, edge: any) => (
                <Popconfirm
                  title="Delete this edge?"
                  onConfirm={() => handleDeleteEdge(edge.id)}
                  okText="Yes"
                  cancelText="No"
                >
                  <Button type="link" danger size="small" icon={<DeleteOutlined />} />
                </Popconfirm>
              ),
            },
          ]}
        />
      </Card>

      {/* Create/Edit Concept Modal */}
      <Modal
        title={editingConcept ? 'Edit Concept' : 'Create Concept'}
        open={conceptModalOpen}
        onCancel={closeConceptModal}
        onOk={handleConceptSubmit}
        confirmLoading={createConcept.isPending || updateConcept.isPending}
        width={isMobile ? '100%' : 560}
        destroyOnClose
      >
        <Form form={conceptForm} layout="vertical">
          <Row gutter={16}>
            <Col xs={24} sm={12}>
              <Form.Item
                name="name"
                label="Name (identifier)"
                rules={[
                  { required: true, message: 'Required' },
                  { pattern: /^[a-z][a-z0-9_]*$/, message: 'Must be snake_case (e.g. error_handling)' },
                ]}
              >
                <Input placeholder="e.g. error_handling" disabled={!!editingConcept} />
              </Form.Item>
            </Col>
            <Col xs={24} sm={12}>
              <Form.Item
                name="displayName"
                label="Display Name"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Input placeholder="e.g. Error Handling" />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item name="description" label="Description">
            <Input.TextArea rows={3} placeholder="Detailed description of the concept..." />
          </Form.Item>

          <Row gutter={16}>
            <Col xs={24} sm={12}>
              <Form.Item
                name="topicGroup"
                label="Topic Group"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Select options={TOPIC_GROUPS} placeholder="Select topic group" />
              </Form.Item>
            </Col>
            <Col xs={24} sm={12}>
              <Form.Item
                name="difficultyTier"
                label="Difficulty Tier"
                rules={[{ required: true, message: 'Required' }]}
              >
                <Select options={TIER_OPTIONS} placeholder="Select tier" />
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Modal>

      {/* Add Edge Modal */}
      <Modal
        title="Add Prerequisite Edge"
        open={edgeModalOpen}
        onCancel={() => { setEdgeModalOpen(false); edgeForm.resetFields(); }}
        onOk={handleEdgeSubmit}
        confirmLoading={createEdge.isPending}
        width={isMobile ? '100%' : 480}
        destroyOnClose
      >
        <Form form={edgeForm} layout="vertical">
          <Form.Item
            name="fromConceptId"
            label="Prerequisite (must learn first)"
            rules={[{ required: true, message: 'Select the prerequisite concept' }]}
          >
            <Select
              showSearch
              placeholder="Select prerequisite concept"
              options={(concepts ?? []).map((c) => ({
                label: `${c.displayName} (Tier ${c.difficultyTier})`,
                value: c.id,
              }))}
              filterOption={(input, option) =>
                (option?.label as string)?.toLowerCase().includes(input.toLowerCase()) ?? false
              }
            />
          </Form.Item>
          <div style={{ textAlign: 'center', margin: '8px 0' }}>
            <ArrowRightOutlined style={{ fontSize: 20, color: '#999' }} />
          </div>
          <Form.Item
            name="toConceptId"
            label="Dependent (requires the prerequisite)"
            rules={[{ required: true, message: 'Select the dependent concept' }]}
          >
            <Select
              showSearch
              placeholder="Select dependent concept"
              options={(concepts ?? []).map((c) => ({
                label: `${c.displayName} (Tier ${c.difficultyTier})`,
                value: c.id,
              }))}
              filterOption={(input, option) =>
                (option?.label as string)?.toLowerCase().includes(input.toLowerCase()) ?? false
              }
            />
          </Form.Item>
          <Text type="secondary" style={{ fontSize: 12 }}>
            The prerequisite must be same or lower tier than the dependent. Cycles are not allowed.
          </Text>
        </Form>
      </Modal>
    </div>
  );
}

export default ConceptManage;
