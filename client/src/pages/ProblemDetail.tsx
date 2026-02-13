import { useParams } from 'react-router-dom';
import { Row, Col, Card, Typography, Tag, Button, Input, Select, Space, Spin } from 'antd';
import { PlayCircleOutlined } from '@ant-design/icons';
import { useProblem } from '../api/queries/useProblems';

const { Title, Paragraph } = Typography;
const { TextArea } = Input;

const difficultyColors: Record<string, string> = {
  EASY: 'green',
  MEDIUM: 'orange',
  HARD: 'red',
};

function ProblemDetail() {
  const { id } = useParams<{ id: string }>();
  const { data: problem, isLoading } = useProblem(id!);

  if (isLoading) {
    return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />;
  }

  if (!problem) {
    return <Title level={4}>Problem not found</Title>;
  }

  return (
    <Row gutter={16}>
      <Col xs={24} lg={12}>
        <Card>
          <Space direction="vertical" size="middle" style={{ width: '100%' }}>
            <div>
              <Title level={3}>{problem.title}</Title>
              <Tag color={difficultyColors[problem.difficulty]}>{problem.difficulty}</Tag>
              {problem.tags?.map((tag: string) => (
                <Tag key={tag}>{tag}</Tag>
              ))}
            </div>
            <Paragraph>{problem.description}</Paragraph>
          </Space>
        </Card>
      </Col>
      <Col xs={24} lg={12}>
        <Card
          title="Code Editor"
          extra={
            <Select defaultValue="python" style={{ width: 120 }}>
              <Select.Option value="python">Python</Select.Option>
              <Select.Option value="javascript">JavaScript</Select.Option>
              <Select.Option value="java">Java</Select.Option>
              <Select.Option value="cpp">C++</Select.Option>
            </Select>
          }
        >
          <TextArea
            rows={16}
            placeholder="Write your code here..."
            style={{ fontFamily: 'monospace', fontSize: 14 }}
          />
          <Button
            type="primary"
            icon={<PlayCircleOutlined />}
            style={{ marginTop: 16 }}
            block
          >
            Submit
          </Button>
        </Card>
      </Col>
    </Row>
  );
}

export default ProblemDetail;
