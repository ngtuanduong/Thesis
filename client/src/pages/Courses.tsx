import { Typography, Card, Row, Col, Button, Tag, Empty, Spin, message } from 'antd';
import {
  BookOutlined,
  TeamOutlined,
  CodeOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';
import { useCourses, useEnrollCourse } from '../api/queries/useInstructor';
import type { CourseItem } from '../api/queries/useInstructor';

const { Title, Text, Paragraph } = Typography;

function CourseCard({ course, onEnroll, enrolling }: {
  course: CourseItem;
  onEnroll: (id: string) => void;
  enrolling: boolean;
}) {
  return (
    <Card
      style={{ height: '100%' }}
      actions={[
        course.isEnrolled ? (
          <span key="enrolled" style={{ color: '#52c41a' }}>
            <CheckCircleOutlined /> Enrolled
          </span>
        ) : (
          <Button
            key="enroll"
            type="link"
            loading={enrolling}
            onClick={() => onEnroll(course.id)}
          >
            Enroll Now
          </Button>
        ),
      ]}
    >
      <Card.Meta
        title={course.title}
        description={
          <>
            {course.description && (
              <Paragraph type="secondary" ellipsis={{ rows: 2 }} style={{ marginBottom: 8 }}>
                {course.description}
              </Paragraph>
            )}
            <div style={{ display: 'flex', gap: 12 }}>
              {course.instructor && (
                <Text type="secondary" style={{ fontSize: 12 }}>
                  <TeamOutlined style={{ marginRight: 4 }} />
                  {course.instructor.name}
                </Text>
              )}
              <Text type="secondary" style={{ fontSize: 12 }}>
                <CodeOutlined style={{ marginRight: 4 }} />
                {course._count?.problems ?? 0} problems
              </Text>
              <Text type="secondary" style={{ fontSize: 12 }}>
                <TeamOutlined style={{ marginRight: 4 }} />
                {course._count?.enrollments ?? 0} students
              </Text>
            </div>
          </>
        }
      />
    </Card>
  );
}

function Courses() {
  const { data: courses, isLoading } = useCourses();
  const enroll = useEnrollCourse();

  const handleEnroll = async (courseId: string) => {
    try {
      await enroll.mutateAsync(courseId);
      message.success('Enrolled successfully!');
    } catch {
      message.error('Failed to enroll');
    }
  };

  if (isLoading) {
    return <Spin size="large" className="center-spin" />;
  }

  const enrolled = (courses ?? []).filter((c) => c.isEnrolled);
  const available = (courses ?? []).filter((c) => !c.isEnrolled);

  return (
    <div>
      <Title level={3}>
        <BookOutlined style={{ marginRight: 8 }} />
        My Courses
      </Title>

      {enrolled.length === 0 ? (
        <Empty
          description="You haven't enrolled in any courses yet. Browse available courses below."
          style={{ marginBottom: 24 }}
        />
      ) : (
        <Row gutter={[16, 16]} style={{ marginBottom: 32 }}>
          {enrolled.map((course) => (
            <Col xs={24} sm={12} lg={8} key={course.id}>
              <CourseCard
                course={course}
                onEnroll={handleEnroll}
                enrolling={enroll.isPending}
              />
            </Col>
          ))}
        </Row>
      )}

      {available.length > 0 && (
        <>
          <Title level={4}>
            Available Courses
            <Tag style={{ marginLeft: 8 }}>{available.length}</Tag>
          </Title>
          <Row gutter={[16, 16]}>
            {available.map((course) => (
              <Col xs={24} sm={12} lg={8} key={course.id}>
                <CourseCard
                  course={course}
                  onEnroll={handleEnroll}
                  enrolling={enroll.isPending}
                />
              </Col>
            ))}
          </Row>
        </>
      )}
    </div>
  );
}

export default Courses;
