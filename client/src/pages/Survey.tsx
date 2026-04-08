import { useState } from 'react';
import { Card, Typography, Radio, Button, Space, message, Result, Divider } from 'antd';
import type { RadioChangeEvent } from 'antd';
import { logEvent } from '../utils/eventLogger';

const { Title, Text, Paragraph } = Typography;

// System Usability Scale (SUS) — 10 standard questions
const SUS_QUESTIONS = [
  'I think that I would like to use this system frequently.',
  'I found the system unnecessarily complex.',
  'I thought the system was easy to use.',
  'I think that I would need the support of a technical person to be able to use this system.',
  'I found the various functions in this system were well integrated.',
  'I thought there was too much inconsistency in this system.',
  'I would imagine that most people would learn to use this system very quickly.',
  'I found the system very cumbersome to use.',
  'I felt very confident using the system.',
  'I needed to learn a lot of things before I could get going with this system.',
];

const SCALE_LABELS = [
  'Strongly Disagree',
  'Disagree',
  'Neutral',
  'Agree',
  'Strongly Agree',
];

function Survey() {
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [submitted, setSubmitted] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (questionIndex: number, e: RadioChangeEvent) => {
    setAnswers((prev) => ({ ...prev, [questionIndex]: e.target.value as number }));
  };

  const allAnswered = SUS_QUESTIONS.every((_, idx) => answers[idx] !== undefined);

  const calculateSUSScore = (): number => {
    let total = 0;
    for (let i = 0; i < SUS_QUESTIONS.length; i++) {
      const raw = answers[i];
      if (raw === undefined) return 0;
      // Odd questions (1,3,5,7,9 — 0-indexed: 0,2,4,6,8): score = raw - 1
      // Even questions (2,4,6,8,10 — 0-indexed: 1,3,5,7,9): score = 5 - raw
      if (i % 2 === 0) {
        total += raw - 1;
      } else {
        total += 5 - raw;
      }
    }
    return total * 2.5; // SUS score range: 0-100
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    try {
      const susScore = calculateSUSScore();
      logEvent('sus_survey_completed', {
        answers,
        susScore,
        timestamp: new Date().toISOString(),
      });
      setSubmitted(true);
      message.success('Survey submitted successfully. Thank you!');
    } catch {
      message.error('Failed to submit survey. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (submitted) {
    const score = calculateSUSScore();
    return (
      <Result
        status="success"
        title="Thank you for your feedback!"
        subTitle={`Your SUS score: ${score.toFixed(1)}/100`}
        extra={
          <Text type="secondary">
            Your responses have been recorded and will help improve the platform.
          </Text>
        }
      />
    );
  }

  return (
    <div style={{ maxWidth: 800, margin: '0 auto' }}>
      <Title level={3}>System Usability Survey</Title>
      <Paragraph type="secondary">
        Please rate the following statements about your experience with AdaptLearn.
        There are no right or wrong answers — we value your honest feedback.
      </Paragraph>

      <Divider />

      {SUS_QUESTIONS.map((question, idx) => (
        <Card
          key={idx}
          size="small"
          style={{ marginBottom: 16 }}
          styles={{ body: { padding: '16px 24px' } }}
        >
          <div style={{ marginBottom: 12 }}>
            <Text strong>
              {idx + 1}. {question}
            </Text>
          </div>
          <Radio.Group
            onChange={(e) => handleChange(idx, e)}
            value={answers[idx]}
          >
            <Space direction="vertical">
              {SCALE_LABELS.map((label, value) => (
                <Radio key={value} value={value + 1}>
                  {value + 1} — {label}
                </Radio>
              ))}
            </Space>
          </Radio.Group>
        </Card>
      ))}

      <div style={{ textAlign: 'center', marginTop: 24, marginBottom: 48 }}>
        <Button
          type="primary"
          size="large"
          onClick={handleSubmit}
          disabled={!allAnswered}
          loading={submitting}
        >
          Submit Survey
        </Button>
        {!allAnswered && (
          <div style={{ marginTop: 8 }}>
            <Text type="secondary">
              Please answer all {SUS_QUESTIONS.length} questions to submit.
              ({Object.keys(answers).length}/{SUS_QUESTIONS.length} answered)
            </Text>
          </div>
        )}
      </div>
    </div>
  );
}

export default Survey;
