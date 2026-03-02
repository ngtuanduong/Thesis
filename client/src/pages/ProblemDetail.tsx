import { useState, useMemo, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import {
  Typography,
  Tag,
  Button,
  Select,
  Space,
  Spin,
  Tabs,
  Table,
  theme,
  message,
  Splitter,
} from 'antd';
import {
  PlayCircleOutlined,
  SendOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  ClockCircleOutlined,
  UndoOutlined,
  LoadingOutlined,
} from '@ant-design/icons';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { oneDark } from '@codemirror/theme-one-dark';
import { useProblem, useSubmitCode } from '../api/queries/useProblems';
import { useProblemSubmissions, useSubmission } from '../api/queries/useSubmissions';
import HintPanel from '../components/HintPanel';
import type { Submission } from '../types';

const { Title, Text, Paragraph } = Typography;

const difficultyColors: Record<string, string> = {
  EASY: 'green',
  MEDIUM: 'orange',
  HARD: 'red',
};

const statusConfig: Record<string, { color: string; icon: React.ReactNode }> = {
  ACCEPTED: { color: '#52c41a', icon: <CheckCircleOutlined /> },
  WRONG_ANSWER: { color: '#ff4d4f', icon: <CloseCircleOutlined /> },
  TIME_LIMIT: { color: '#faad14', icon: <ClockCircleOutlined /> },
  RUNTIME_ERROR: { color: '#ff4d4f', icon: <CloseCircleOutlined /> },
  COMPILATION_ERROR: { color: '#ff4d4f', icon: <CloseCircleOutlined /> },
  PENDING: { color: '#1677ff', icon: <LoadingOutlined /> },
  RUNNING: { color: '#1677ff', icon: <LoadingOutlined /> },
};

const DEFAULT_CODE = `def solution():
    # Write your code here
    pass
`;

function ProblemDetail() {
  const { id } = useParams<{ id: string }>();
  const { token: themeToken } = theme.useToken();
  const { data: problem, isLoading } = useProblem(id!);
  const submitCode = useSubmitCode();
  const { data: submissions, refetch: refetchSubmissions } = useProblemSubmissions(id!);

  const [code, setCode] = useState(DEFAULT_CODE);
  const [language, setLanguage] = useState('python');
  const [activeTab, setActiveTab] = useState('description');
  const [pollingId, setPollingId] = useState<string | undefined>(undefined);
  // Ref tracks the last submission we already notified about so StrictMode's
  // double-invoke of effects doesn't fire duplicate toasts.
  const notifiedSubmissionRef = useRef<string | undefined>(undefined);

  // Poll the active submission until it reaches a terminal state
  const { data: polledSubmission } = useSubmission(pollingId, {
    refetchInterval: pollingId ? 1000 : false,
  });

  // Stop polling once we get a terminal status
  useEffect(() => {
    if (
      polledSubmission &&
      pollingId &&
      polledSubmission.id !== notifiedSubmissionRef.current &&
      polledSubmission.status !== 'PENDING' &&
      polledSubmission.status !== 'RUNNING'
    ) {
      notifiedSubmissionRef.current = polledSubmission.id;
      setPollingId(undefined);
      refetchSubmissions();
      if (polledSubmission.status === 'ACCEPTED') {
        message.success('All test cases passed!');
      } else {
        message.error(`Submission: ${polledSubmission.status.replace(/_/g, ' ')}`);
      }
    }
  }, [polledSubmission?.status, polledSubmission?.id, pollingId]); // eslint-disable-line react-hooks/exhaustive-deps

  const latestResult = polledSubmission ?? null;
  const isRunning =
    submitCode.isPending ||
    latestResult?.status === 'RUNNING' ||
    latestResult?.status === 'PENDING';

  const visibleTestCases = useMemo(
    () => problem?.testCases?.filter((tc) => !tc.isHidden) ?? [],
    [problem?.testCases],
  );

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
      setPollingId(result.id);
    } catch (error: any) {
      message.error(error.response?.data?.message || 'Submission failed');
    }
  };

  const handleReset = () => {
    setCode(DEFAULT_CODE);
  };

  const submissionColumns = [
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => {
        const cfg = statusConfig[status];
        return (
          <Space>
            <span style={{ color: cfg?.color }}>{cfg?.icon}</span>
            <Text style={{ color: cfg?.color }}>
              {status.replace(/_/g, ' ')}
            </Text>
          </Space>
        );
      },
    },
    {
      title: 'Language',
      dataIndex: 'language',
      key: 'language',
      render: (lang: string) => <Tag>{lang}</Tag>,
    },
    {
      title: 'Runtime',
      dataIndex: 'runtime',
      key: 'runtime',
      render: (val: number | null) => (val != null ? `${val} ms` : '-'),
    },
    {
      title: 'Submitted',
      dataIndex: 'createdAt',
      key: 'createdAt',
      render: (val: string) => new Date(val).toLocaleString(),
    },
  ];

  if (isLoading) {
    return <Spin size="large" style={{ display: 'block', margin: '100px auto' }} />;
  }

  if (!problem) {
    return <Title level={4}>Problem not found</Title>;
  }

  // ---------- Left panel: description / submissions ----------
  const leftPanel = (
    <div style={{ height: '100%', overflow: 'auto', padding: '16px 20px' }}>
      <Tabs
        activeKey={activeTab}
        onChange={setActiveTab}
        items={[
          {
            key: 'description',
            label: 'Description',
            children: (
              <div>
                <Title level={4} style={{ marginTop: 0 }}>
                  {problem.title}
                </Title>
                <Space style={{ marginBottom: 16 }}>
                  <Tag color={difficultyColors[problem.difficulty]}>
                    {problem.difficulty}
                  </Tag>
                  {problem.tags?.map((tag: string) => (
                    <Tag key={tag}>{tag}</Tag>
                  ))}
                </Space>

                <Paragraph style={{ whiteSpace: 'pre-wrap', fontSize: 14, lineHeight: 1.8 }}>
                  {problem.description}
                </Paragraph>

                {visibleTestCases.length > 0 && (
                  <div style={{ marginTop: 24 }}>
                    <Title level={5}>Examples</Title>
                    {visibleTestCases.map((tc, idx) => (
                      <div
                        key={tc.id}
                        style={{
                          background: themeToken.colorBgLayout,
                          borderRadius: 8,
                          padding: '12px 16px',
                          marginBottom: 12,
                          fontFamily: 'monospace',
                          fontSize: 13,
                        }}
                      >
                        <Text strong>Example {idx + 1}</Text>
                        <div style={{ marginTop: 8 }}>
                          <Text type="secondary">Input: </Text>
                          <Text code>{tc.input}</Text>
                        </div>
                        <div style={{ marginTop: 4 }}>
                          <Text type="secondary">Expected: </Text>
                          <Text code>{tc.expected}</Text>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ),
          },
          {
            key: 'submissions',
            label: `Submissions${submissions?.length ? ` (${submissions.length})` : ''}`,
            children: (
              <Table
                dataSource={submissions ?? []}
                columns={submissionColumns}
                rowKey="id"
                size="small"
                pagination={{ pageSize: 10 }}
                onRow={(record: Submission) => ({
                  onClick: () => {
                    setCode(record.code);
                    setLanguage(record.language);
                    message.info('Loaded submission code into editor');
                  },
                  style: { cursor: 'pointer' },
                })}
              />
            ),
          },
        ]}
      />
    </div>
  );

  // ---------- Right panel: editor + results ----------
  const editorToolbar = (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '8px 12px',
        borderBottom: `1px solid ${themeToken.colorBorderSecondary}`,
        background: themeToken.colorBgLayout,
      }}
    >
      <Select
        value={language}
        onChange={setLanguage}
        style={{ width: 130 }}
        size="small"
        options={[
          { value: 'python', label: 'Python' },
          { value: 'javascript', label: 'JavaScript', disabled: true },
          { value: 'java', label: 'Java', disabled: true },
          { value: 'cpp', label: 'C++', disabled: true },
        ]}
      />
      <Button size="small" icon={<UndoOutlined />} onClick={handleReset}>
        Reset
      </Button>
    </div>
  );

  const resultsToolbar = (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '8px 12px',
        borderBottom: `1px solid ${themeToken.colorBorderSecondary}`,
        background: themeToken.colorBgLayout,
      }}
    >
      <Text strong style={{ fontSize: 13 }}>
        Results
      </Text>
      <Space>
        <Button
          size="small"
          icon={<PlayCircleOutlined />}
          onClick={handleSubmit}
          loading={isRunning}
        >
          Run
        </Button>
        <Button
          type="primary"
          size="small"
          icon={<SendOutlined />}
          onClick={handleSubmit}
          loading={isRunning}
        >
          Submit
        </Button>
      </Space>
    </div>
  );

  const resultDisplay = (
    <div style={{ padding: 12, overflow: 'auto', flex: 1 }}>
      {latestResult ? (
        <div>
          <Space style={{ marginBottom: 12 }}>
            <span style={{ color: statusConfig[latestResult.status]?.color, fontSize: 18 }}>
              {statusConfig[latestResult.status]?.icon}
            </span>
            <Text
              strong
              style={{
                color: statusConfig[latestResult.status]?.color,
                fontSize: 16,
              }}
            >
              {latestResult.status.replace(/_/g, ' ')}
            </Text>
            {latestResult.runtime != null && (
              <Text type="secondary">({latestResult.runtime} ms)</Text>
            )}
            {latestResult.memory != null && (
              <Text type="secondary">({latestResult.memory} MB)</Text>
            )}
          </Space>
          {latestResult.output && (
            <div
              style={{
                background: '#1e1e1e',
                color: '#d4d4d4',
                borderRadius: 6,
                padding: 12,
                fontFamily: 'monospace',
                fontSize: 13,
                whiteSpace: 'pre-wrap',
                maxHeight: 200,
                overflow: 'auto',
              }}
            >
              {latestResult.output}
            </div>
          )}
        </div>
      ) : (
        <Text type="secondary" style={{ fontSize: 13 }}>
          Submit your code to see results here.
        </Text>
      )}
    </div>
  );

  const rightPanel = (
    <Splitter layout="vertical" style={{ height: '100%' }}>
      <Splitter.Panel defaultSize="65%" min="30%">
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          {editorToolbar}
          <div style={{ flex: 1, overflow: 'auto' }}>
            <CodeMirror
              value={code}
              onChange={setCode}
              extensions={[python()]}
              theme={oneDark}
              height="100%"
              style={{ height: '100%' }}
              basicSetup={{
                lineNumbers: true,
                bracketMatching: true,
                foldGutter: true,
                highlightActiveLine: true,
                autocompletion: true,
              }}
            />
          </div>
        </div>
      </Splitter.Panel>
      <Splitter.Panel defaultSize="35%" min="15%">
        <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          {resultsToolbar}
          {resultDisplay}
          <div style={{ padding: '0 12px 8px' }}>
            <HintPanel
              problemId={id!}
              code={code}
              errorMessage={latestResult?.output || undefined}
            />
          </div>
        </div>
      </Splitter.Panel>
    </Splitter>
  );

  return (
    <div style={{ height: 'calc(100vh - 160px)', margin: -24 }}>
      <Splitter style={{ height: '100%' }}>
        <Splitter.Panel defaultSize="45%" min="25%">
          {leftPanel}
        </Splitter.Panel>
        <Splitter.Panel defaultSize="55%" min="30%">
          {rightPanel}
        </Splitter.Panel>
      </Splitter>
    </div>
  );
}

export default ProblemDetail;
