import { useState, useMemo, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
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
import { useResponsive } from '../hooks/useResponsive';
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
import styles from './ProblemDetail.module.css';

const { Title, Text } = Typography;

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

const FALLBACK_CODE = `def solution():
    # Write your code here
    pass
`;

function ProblemDetail() {
  const { id } = useParams<{ id: string }>();
  const { token: themeToken } = theme.useToken();
  const { isMobile } = useResponsive();
  const { data: problem, isLoading } = useProblem(id!);
  const submitCode = useSubmitCode();
  const { data: submissions, refetch: refetchSubmissions } = useProblemSubmissions(id!);

  const effectiveStarterCode = problem?.starterCode || FALLBACK_CODE;
  const [code, setCode] = useState(FALLBACK_CODE);
  const [language, setLanguage] = useState('python');

  // Load problem-specific starter code when problem data arrives
  useEffect(() => {
    if (problem?.starterCode) {
      setCode(problem.starterCode);
    }
  }, [problem?.starterCode]);
  const [activeTab, setActiveTab] = useState('description');
  const [mobileTab, setMobileTab] = useState<'problem' | 'code'>('problem');
  const [pollingId, setPollingId] = useState<string | undefined>(undefined);
  const [lastResult, setLastResult] = useState<Submission | null>(null);
  // Ref tracks the last submission we already notified about so StrictMode's
  // double-invoke of effects doesn't fire duplicate toasts.
  const notifiedSubmissionRef = useRef<string | undefined>(undefined);

  // Poll the active submission until it reaches a terminal state
  const { data: polledSubmission } = useSubmission(pollingId, {
    refetchInterval: pollingId ? 1000 : false,
  });

  // Preserve the polled submission in state so it persists after polling stops
  useEffect(() => {
    if (polledSubmission) {
      setLastResult(polledSubmission);
    }
  }, [polledSubmission]);

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

  const latestResult = polledSubmission ?? lastResult;
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
    setCode(effectiveStarterCode);
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
    return <Spin size="large" className="center-spin" />;
  }

  if (!problem) {
    return <Title level={4}>Problem not found</Title>;
  }

  // ---------- Left panel: description / submissions ----------
  const leftPanel = (
    <div className={styles.leftPanel}>
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
                  {(problem as any).problemConcepts?.map((pc: any) => (
                    <Tag key={pc.concept?.id} color={pc.isPrimary ? 'blue' : 'default'}>
                      {pc.concept?.displayName}
                    </Tag>
                  ))}
                </Space>

                {/* Description — rendered as markdown */}
                <Title level={5}>Description</Title>
                <div className={styles.markdownContent}>
                  <ReactMarkdown>{problem.description}</ReactMarkdown>
                </div>

                {/* Examples — from visible test cases */}
                {visibleTestCases.length > 0 && (
                  <div className="section-gap-lg">
                    <Title level={5}>Examples</Title>
                    {visibleTestCases.map((tc, idx) => (
                      <div
                        key={tc.id}
                        className={styles.exampleBlock}
                        style={{ background: themeToken.colorBgLayout }}
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

                {/* Constraints */}
                {problem.constraints && (
                  <div className="section-gap-lg">
                    <Title level={5}>Constraints</Title>
                    <div className={styles.markdownContent}>
                      <ReactMarkdown>{problem.constraints}</ReactMarkdown>
                    </div>
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
      className={styles.panelToolbar}
      style={{ borderBottom: `1px solid ${themeToken.colorBorderSecondary}`, background: themeToken.colorBgLayout }}
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
      className={styles.panelToolbar}
      style={{ borderBottom: `1px solid ${themeToken.colorBorderSecondary}`, background: themeToken.colorBgLayout }}
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
    <div className={styles.resultContent}>
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
            <div className={styles.codeOutput}>
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
        <div className={styles.columnFull}>
          {editorToolbar}
          <div className={styles.flexGrow}>
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
        <div className={styles.columnFull}>
          {resultsToolbar}
          {resultDisplay}
          <div className={styles.hintFooter}>
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

  if (isMobile) {
    return (
      <div className={styles.mobileWrapper}>
        <Tabs
          activeKey={mobileTab}
          onChange={(key) => setMobileTab(key as 'problem' | 'code')}
          style={{ flex: 1, display: 'flex', flexDirection: 'column' }}
          items={[
            {
              key: 'problem',
              label: 'Problem',
              children: (
                <div className={styles.mobileProblemScroll}>
                  {leftPanel}
                </div>
              ),
            },
            {
              key: 'code',
              label: 'Code',
              children: (
                <div className={styles.mobileCodePanel}>
                  {editorToolbar}
                  <div className={styles.flexGrowHidden}>
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
                  {latestResult && (
                    <div className={styles.mobileResultPreview}>
                      {resultDisplay}
                    </div>
                  )}
                  <div className={styles.mobileActions} style={{ borderTop: `1px solid ${themeToken.colorBorderSecondary}` }}>
                    <Button
                      block
                      icon={<PlayCircleOutlined />}
                      onClick={handleSubmit}
                      loading={isRunning}
                    >
                      Run
                    </Button>
                    <Button
                      block
                      type="primary"
                      icon={<SendOutlined />}
                      onClick={handleSubmit}
                      loading={isRunning}
                    >
                      Submit
                    </Button>
                  </div>
                  <div className={styles.hintFooter}>
                    <HintPanel
                      problemId={id!}
                      code={code}
                      errorMessage={latestResult?.output || undefined}
                    />
                  </div>
                </div>
              ),
            },
          ]}
        />
      </div>
    );
  }

  return (
    <div className={styles.desktopWrapper}>
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
