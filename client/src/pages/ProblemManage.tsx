import { useState, useEffect, useCallback } from 'react';
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
  message,
  Row,
  Col,
  Checkbox,
} from 'antd';
import {
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  MinusCircleOutlined,
  SearchOutlined,
} from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import type { Problem } from '../types';
import {
  useProblemsPaginated,
  useCreateProblem,
  useUpdateProblem,
  useDeleteProblem,
} from '../api/queries/useProblemManage';
import { useResponsive } from '../hooks/useResponsive';

const { Title } = Typography;
const { TextArea } = Input;

const difficultyColors: Record<string, string> = {
  EASY: 'green',
  MEDIUM: 'orange',
  HARD: 'red',
};

interface ProblemFormValues {
  title: string;
  description: string;
  difficulty: 'EASY' | 'MEDIUM' | 'HARD';
  tags?: string[];
  starterCode?: string;
  testCases?: { input: string; expected: string; isHidden: boolean }[];
}

function ProblemManage() {
  const [form] = Form.useForm<ProblemFormValues>();
  const [modalOpen, setModalOpen] = useState(false);
  const [editingProblem, setEditingProblem] = useState<Problem | null>(null);
  const [searchText, setSearchText] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(15);
  const { isMobile } = useResponsive();

  // Debounce search
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchText);
      setPage(1);
    }, 300);
    return () => clearTimeout(timer);
  }, [searchText]);

  const { data, isLoading, isFetching } = useProblemsPaginated({
    page,
    pageSize,
    search: debouncedSearch || undefined,
  });
  const createProblem = useCreateProblem();
  const updateProblem = useUpdateProblem();
  const deleteProblem = useDeleteProblem();

  const openCreateModal = useCallback(() => {
    setEditingProblem(null);
    form.resetFields();
    form.setFieldsValue({
      difficulty: 'EASY',
      testCases: [{ input: '', expected: '', isHidden: false }],
    });
    setModalOpen(true);
  }, [form]);

  const openEditModal = useCallback(
    (problem: Problem) => {
      setEditingProblem(problem);
      form.setFieldsValue({
        title: problem.title,
        description: problem.description,
        difficulty: problem.difficulty,
        tags: problem.tags ?? [],
        starterCode: problem.starterCode ?? '',
        testCases:
          problem.testCases && problem.testCases.length > 0
            ? problem.testCases.map((tc) => ({
                input: tc.input,
                expected: tc.expected,
                isHidden: tc.isHidden,
              }))
            : [{ input: '', expected: '', isHidden: false }],
      });
      setModalOpen(true);
    },
    [form],
  );

  const closeModal = useCallback(() => {
    setModalOpen(false);
    setEditingProblem(null);
    form.resetFields();
  }, [form]);

  const handleSubmit = useCallback(async () => {
    try {
      const values = await form.validateFields();
      const payload = {
        title: values.title,
        description: values.description,
        difficulty: values.difficulty,
        tags: values.tags,
        starterCode: values.starterCode?.trim() || undefined,
        testCases: values.testCases?.filter(
          (tc) => tc.input.trim() !== '' || tc.expected.trim() !== '',
        ),
      };

      if (editingProblem) {
        await updateProblem.mutateAsync({ id: editingProblem.id, ...payload });
        message.success('Problem updated successfully');
      } else {
        await createProblem.mutateAsync(payload);
        message.success('Problem created successfully');
      }
      closeModal();
    } catch (err) {
      if (err && typeof err === 'object' && 'errorFields' in err) {
        return; // validation error, form will show messages
      }
      message.error('Failed to save problem');
    }
  }, [form, editingProblem, createProblem, updateProblem, closeModal]);

  const handleDelete = useCallback(
    async (id: string) => {
      try {
        await deleteProblem.mutateAsync(id);
        message.success('Problem deleted successfully');
      } catch {
        message.error('Failed to delete problem');
      }
    },
    [deleteProblem],
  );

  const columns: ColumnsType<Problem> = [
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      sorter: (a, b) => a.title.localeCompare(b.title),
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
      responsive: ['md'] as any,
      render: (tags: string[]) => (
        <Space size={[0, 4]} wrap>
          {tags?.map((tag) => (
            <Tag key={tag}>{tag}</Tag>
          ))}
        </Space>
      ),
    },
    {
      title: 'Test Cases',
      key: 'testCases',
      width: 110,
      responsive: ['md'] as any,
      render: (_: unknown, record: Problem) => record.testCases?.length ?? 0,
    },
    {
      title: 'Actions',
      key: 'actions',
      width: 150,
      render: (_: unknown, record: Problem) => (
        <Space>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => openEditModal(record)}
          >
            Edit
          </Button>
          <Popconfirm
            title="Delete problem"
            description="Are you sure you want to delete this problem?"
            onConfirm={() => handleDelete(record.id)}
            okText="Yes"
            cancelText="No"
          >
            <Button type="link" danger icon={<DeleteOutlined />}>
              Delete
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  const isSubmitting = createProblem.isPending || updateProblem.isPending;

  return (
    <div>
      <div className="responsive-page-header">
        <Title level={3} style={{ margin: 0 }}>
          Problem Management
        </Title>
        <Space>
          <Input
            placeholder="Search by title..."
            prefix={<SearchOutlined />}
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            style={{ width: isMobile ? '100%' : 250 }}
            allowClear
          />
          <Button type="primary" icon={<PlusOutlined />} onClick={openCreateModal}>
            Create Problem
          </Button>
        </Space>
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
      />

      <Modal
        title={editingProblem ? 'Edit Problem' : 'Create Problem'}
        open={modalOpen}
        onCancel={closeModal}
        onOk={handleSubmit}
        confirmLoading={isSubmitting}
        width={isMobile ? '100%' : 720}
        destroyOnClose
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            difficulty: 'EASY',
            testCases: [{ input: '', expected: '', isHidden: false }],
          }}
        >
          <Form.Item
            name="title"
            label="Title"
            rules={[{ required: true, message: 'Please enter a title' }]}
          >
            <Input placeholder="Problem title" />
          </Form.Item>

          <Form.Item
            name="description"
            label="Description"
            rules={[{ required: true, message: 'Please enter a description' }]}
          >
            <TextArea rows={6} placeholder="Problem description (supports markdown)" />
          </Form.Item>

          <Row gutter={16}>
            <Col xs={24} sm={12}>
              <Form.Item
                name="difficulty"
                label="Difficulty"
                rules={[{ required: true, message: 'Please select difficulty' }]}
              >
                <Select>
                  <Select.Option value="EASY">Easy</Select.Option>
                  <Select.Option value="MEDIUM">Medium</Select.Option>
                  <Select.Option value="HARD">Hard</Select.Option>
                </Select>
              </Form.Item>
            </Col>
            <Col xs={24} sm={12}>
              <Form.Item name="tags" label="Tags">
                <Select
                  mode="tags"
                  placeholder="Type and press Enter to add tags"
                  tokenSeparators={[',']}
                />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="starterCode"
            label="Starter Code"
            extra="Leave empty to auto-generate from test cases. Function must be named 'solution'."
          >
            <TextArea
              rows={4}
              placeholder={'def solution(nums, target):\n    # Write your code here\n    pass'}
              style={{ fontFamily: 'monospace', fontSize: 13 }}
            />
          </Form.Item>

          <Typography.Text strong style={{ display: 'block', marginBottom: 8 }}>
            Test Cases
          </Typography.Text>
          <Form.List name="testCases">
            {(fields, { add, remove }) => (
              <>
                {fields.map(({ key, name, ...restField }) => (
                  <Row key={key} gutter={8} align="middle" style={{ marginBottom: 8 }}>
                    <Col xs={24} sm={9}>
                      <Form.Item
                        {...restField}
                        name={[name, 'input']}
                        style={{ marginBottom: 0 }}
                      >
                        <Input placeholder="Input" />
                      </Form.Item>
                    </Col>
                    <Col xs={24} sm={9}>
                      <Form.Item
                        {...restField}
                        name={[name, 'expected']}
                        style={{ marginBottom: 0 }}
                      >
                        <Input placeholder="Expected Output" />
                      </Form.Item>
                    </Col>
                    <Col xs={12} sm={4}>
                      <Form.Item
                        {...restField}
                        name={[name, 'isHidden']}
                        valuePropName="checked"
                        style={{ marginBottom: 0 }}
                      >
                        <Checkbox>Hidden</Checkbox>
                      </Form.Item>
                    </Col>
                    <Col xs={12} sm={2}>
                      {fields.length > 1 && (
                        <MinusCircleOutlined
                          style={{ color: '#ff4d4f', fontSize: 18, cursor: 'pointer' }}
                          onClick={() => remove(name)}
                        />
                      )}
                    </Col>
                  </Row>
                ))}
                <Form.Item>
                  <Button
                    type="dashed"
                    onClick={() => add({ input: '', expected: '', isHidden: false })}
                    block
                    icon={<PlusOutlined />}
                  >
                    Add Test Case
                  </Button>
                </Form.Item>
              </>
            )}
          </Form.List>
        </Form>
      </Modal>
    </div>
  );
}

export default ProblemManage;
