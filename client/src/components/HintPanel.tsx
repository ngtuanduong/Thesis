import { useState } from 'react';
import { Button, Card, Tag, Typography, Space, Spin, Alert } from 'antd';
import { BulbOutlined } from '@ant-design/icons';
import { useGenerateHint } from '../api/queries/useAdaptive';
import { useMe } from '../api/queries/useAuth';

import styles from './HintPanel.module.css';

const { Text, Paragraph } = Typography;

interface HintPanelProps {
  problemId: string;
  code: string;
  errorMessage?: string;
}

function HintPanel({ problemId, code, errorMessage }: HintPanelProps) {
  const { data: user } = useMe();
  const generateHint = useGenerateHint();
  const [hintLevel, setHintLevel] = useState(1);
  const [hints, setHints] = useState<
    { hint: string; level: number; concepts: string[] }[]
  >([]);

  const handleGetHint = async () => {
    if (!user?.id || !code.trim()) return;

    try {
      const result = await generateHint.mutateAsync({
        studentId: user.id,
        problemId,
        code,
        errorMessage,
        hintLevel,
      });

      if (result.hint) {
        setHints((prev) => [
          ...prev,
          {
            hint: result.hint!,
            level: result.hint_level,
            concepts: result.concepts_referenced,
          },
        ]);
        setHintLevel((prev) => Math.min(prev + 1, 3));
      }
    } catch {
      // Error handled by mutation state
    }
  };

  const levelLabels = ['Gentle Nudge', 'Specific Hint', 'Detailed Guide'];

  return (
    <Card
      size="small"
      title={
        <Space>
          <BulbOutlined style={{ color: '#faad14' }} />
          <Text strong>AI Tutor</Text>
        </Space>
      }
      extra={
        <Button
          size="small"
          type="primary"
          icon={<BulbOutlined />}
          onClick={handleGetHint}
          loading={generateHint.isPending}
          disabled={!code.trim()}
        >
          {hints.length === 0 ? 'Get Hint' : 'More Help'}
        </Button>
      }
      style={{ marginTop: 8 }}
      styles={{ body: { padding: '8px 12px', maxHeight: 250, overflow: 'auto' } }}
    >
      {generateHint.isPending && (
        <div className={styles.loadingCenter}>
          <Spin size="small" />
          <Text type="secondary" style={{ marginLeft: 8 }}>
            Thinking...
          </Text>
        </div>
      )}

      {generateHint.isError && (
        <Alert
          type="warning"
          message="Hints unavailable right now. Keep trying on your own!"
          showIcon
          style={{ marginBottom: 8 }}
        />
      )}

      {hints.length === 0 && !generateHint.isPending && (
        <Text type="secondary" style={{ fontSize: 12 }}>
          Stuck? Click "Get Hint" for a Socratic nudge. Hints get progressively
          more detailed (Level {hintLevel}: {levelLabels[hintLevel - 1]}).
        </Text>
      )}

      {hints.map((h, i) => (
        <div key={i} className={styles.hintCard}>
          <div className={styles.hintCardHeader}>
            <Tag color="gold" style={{ fontSize: 10 }}>
              Level {h.level}: {levelLabels[h.level - 1]}
            </Tag>
            {h.concepts.map((c) => (
              <Tag key={c} style={{ fontSize: 10 }}>
                {c}
              </Tag>
            ))}
          </div>
          <Paragraph
            style={{ margin: 0, fontSize: 13, whiteSpace: 'pre-wrap' }}
          >
            {h.hint}
          </Paragraph>
        </div>
      ))}
    </Card>
  );
}

export default HintPanel;
