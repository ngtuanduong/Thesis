import { useState, useCallback } from 'react';
import {
  Table,
  Modal,
  Form,
  Input,
  Button,
  Popconfirm,
  Space,
  Typography,
  message,
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { ColumnsType } from 'antd/es/table';
import { useCourses, useCreateCourse, useDeleteCourse } from '../api/queries/useInstructor';
import { useResponsive } from '../hooks/useResponsive';

const { Title, Text } = Typography;
const { TextArea } = Input;

interface CourseRow {
  id: string;
  title: string;
  description?: string;
  instructorId: string;
  instructor?: { id: string; name: string };
  _count?: { enrollments: number; problems: number };
  createdAt?: string;
}

function CourseManage() {
  const [form] = Form.useForm();
  const [modalOpen, setModalOpen] = useState(false);
  const [editingCourse, setEditingCourse] = useState<CourseRow | null>(null);
  const { isMobile } = useResponsive();

  const { data: courses, isLoading } = useCourses();
  const createCourse = useCreateCourse();
  const deleteCourse = useDeleteCourse();

  const openCreateModal = useCallback(() => {
    setEditingCourse(null);
    form.resetFields();
    setModalOpen(true);
  }, [form]);

  const openEditModal = useCallback(
    (course: CourseRow) => {
      setEditingCourse(course);
      form.setFieldsValue({ title: course.title, description: course.description });
      setModalOpen(true);
    },
    [form],
  );

  const closeModal = useCallback(() => {
    setModalOpen(false);
    setEditingCourse(null);
    form.resetFields();
  }, [form]);

  const handleSubmit = useCallback(async () => {
    try {
      const values = await form.validateFields();
      if (editingCourse) {
        // Use create hook for now (update can be added later)
        message.info('Update not yet supported — please delete and recreate');
      } else {
        await createCourse.mutateAsync(values);
        message.success('Course created successfully');
      }
      closeModal();
    } catch (err) {
      if (err && typeof err === 'object' && 'errorFields' in err) return;
      message.error('Failed to save course');
    }
  }, [form, editingCourse, createCourse, closeModal]);

  const handleDelete = useCallback(
    async (id: string) => {
      try {
        await deleteCourse.mutateAsync(id);
        message.success('Course deleted successfully');
      } catch {
        message.error('Failed to delete course');
      }
    },
    [deleteCourse],
  );

  const columns: ColumnsType<CourseRow> = [
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      render: (text: string, record: CourseRow) => (
        <div>
          <Text strong>{text}</Text>
          {record.description && (
            <div>
              <Text type="secondary" style={{ fontSize: 12 }}>
                {record.description.length > 80
                  ? `${record.description.slice(0, 80)}...`
                  : record.description}
              </Text>
            </div>
          )}
        </div>
      ),
    },
    {
      title: 'Students',
      key: 'students',
      width: 90,
      align: 'center',
      render: (_: unknown, record: CourseRow) => record._count?.enrollments ?? 0,
    },
    {
      title: 'Problems',
      key: 'problems',
      width: 90,
      align: 'center',
      render: (_: unknown, record: CourseRow) => record._count?.problems ?? 0,
    },
    {
      title: 'Actions',
      key: 'actions',
      width: isMobile ? 80 : 150,
      render: (_: unknown, record: CourseRow) => (
        <Space size={isMobile ? 0 : 'small'}>
          <Button type="link" icon={<EditOutlined />} onClick={() => openEditModal(record)}>
            {!isMobile && 'Edit'}
          </Button>
          <Popconfirm
            title="Delete course?"
            description="This will remove all enrollments. Problems will become unassigned."
            onConfirm={() => handleDelete(record.id)}
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
      <div className="responsive-page-header">
        <Title level={3} style={{ margin: 0 }}>Course Management</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={openCreateModal}>
          Create Course
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={(courses ?? []) as CourseRow[]}
        rowKey="id"
        loading={isLoading}
        pagination={false}
        scroll={{ x: 400 }}
      />

      <Modal
        title={editingCourse ? 'Edit Course' : 'Create Course'}
        open={modalOpen}
        onCancel={closeModal}
        onOk={handleSubmit}
        confirmLoading={createCourse.isPending}
        width={isMobile ? '100%' : 520}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <Form.Item
            name="title"
            label="Title"
            rules={[{ required: true, message: 'Please enter a course title' }]}
          >
            <Input placeholder="e.g. Introduction to Python" />
          </Form.Item>
          <Form.Item name="description" label="Description">
            <TextArea rows={3} placeholder="Course description (optional)" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

export default CourseManage;
