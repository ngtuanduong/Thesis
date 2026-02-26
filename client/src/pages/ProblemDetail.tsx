import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Row, Col, Card, Typography, Tag, Button, Input, Select, Space, Spin, message, Alert } from 'antd';
import { PlayCircleOutlined, CheckCircleOutlined, CloseCircleOutlined, ClockCircleOutlined } from '@ant-design/icons';
import { useProblem, useSubmitCode } from '../api/queries/useProblems';

const { Title, Paragraph, Text } = Typography;
const { TextArea } = Input;

const difficultyColors: Record<string, string> = {
  EASY: 'green',
  MEDIUM: 'orange',
  HARD: 'red',
};

const statusColors: Record<string, string> = {
  ACCEPTED: 'success',
  WRONG_ANSWER: 'error',
  TIME_LIMIT: 'warning',
  RUNTIME_ERROR: 'error',
  PENDING: 'info',
  RUNNING: 'processing',
};

const statusIcons: Record<string, any> = {
  ACCEPTED: <CheckCircleOutlined />,
  WRONG_ANSWER: <CloseCircleOutlined />,
  TIME_LIMIT: <ClockCircleOutlined />,
  RUNTIME_ERROR: <CloseCircleOutlined />,
};

function ProblemDetail() {
  const { id } = useParams<{ id: string }>();
  const { data: problem, isLoading } = useProblem(id!);
  const submitCode = useSubmitCode();

  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [submissionResult, setSubmissionResult] = useState<any>(null);

  const handleSubmit = async () => {
    if (!code.trim()) {
      message.error('Please write some code first!');
      return;
    }

    try {
      const result = await submitCode.mutateAsync({
        problemId: id!,
        code,
        language,
      });

      setSubmissionResult(result);
      message.success('Code submitted! Executing...');

      // Poll for result
      pollSubmissionResult(result.id);
    } catch (error: any) {
      message.error(error.response?.data?.message || 'Submission failed');
    }
  };

  const pollSubmissionResult = async (submissionId: string) => {
    const maxAttempts = 20;
    let attempts = 0;

    const poll = setInterval(async () => {
      try {
        const res = await fetch(`/api/submissions/${submissionId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const data = await res.json();

        if (data.status !== 'PENDING' && data.status !== 'RUNNING') {
          clearInterval(poll);
          setSubmissionResult(data);

          if (data.status === 'ACCEPTED') {
            message.success('All test cases passed! 🎉');
          } else {
            message.error(`Submission ${data.status.replace('_', ' ')}`);
          }
        }

        attempts++;
        if (attempts >= maxAttempts) {
          clearInterval(poll);
        }
      } catch (error) {
        clearInterval(poll);
      }
    }, 1000);
  };

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
            <Select value={language} onChange={setLanguage} style={{ width: 120 }}>
              <Select.Option value="python">Python</Select.Option>
              <Select.Option value="javascript" disabled>JavaScript</Select.Option>
              <Select.Option value="java" disabled>Java</Select.Option>
              <Select.Option value="cpp" disabled>C++</Select.Option>
            </Select>
          }
        >
          <TextArea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            rows={16}
            placeholder="def solution(nums, target):&#10;    # Write your code here&#10;    pass"
            style={{ fontFamily: 'monospace', fontSize: 14 }}
          />
          <Button
            type="primary"
            icon={<PlayCircleOutlined />}
            style={{ marginTop: 16 }}
            block
            onClick={handleSubmit}
            loading={submitCode.isPending || submissionResult?.status === 'RUNNING'}
          >
            {submitCode.isPending || submissionResult?.status === 'RUNNING'
              ? 'Running...'
              : 'Submit'}
          </Button>

          {submissionResult && (
            <Alert
              style={{ marginTop: 16 }}
              message={
                <Space>
                  {statusIcons[submissionResult.status]}
                  <Text strong>{submissionResult.status.replace('_', ' ')}</Text>
                  {submissionResult.runtime && (
                    <Text type="secondary">({submissionResult.runtime}ms)</Text>
                  )}
                </Space>
              }
              description={
                <div style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace', fontSize: 12 }}>
                  {submissionResult.output}
                </div>
              }
              type={statusColors[submissionResult.status] as any}
              showIcon={false}
            />
          )}
        </Card>
      </Col>
    </Row>
  );
}

export default ProblemDetail;
