import { useState, useEffect } from 'react';
import { Modal, Steps, Typography, Button, Space } from 'antd';
import {
  RocketOutlined,
  NodeIndexOutlined,
  TrophyOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';

const { Title, Paragraph } = Typography;

const ONBOARDING_KEY = 'adaptlearn_onboarding_done';

const steps = [
  {
    title: 'Welcome to AdaptLearn',
    icon: <RocketOutlined />,
    content: (
      <div style={{ textAlign: 'center', padding: '24px 0' }}>
        <Title level={4}>Personalized Programming Learning</Title>
        <Paragraph>
          AdaptLearn adapts to your skill level using AI-powered algorithms.
          Problems are selected based on your knowledge state, ensuring you
          always work on the right challenge at the right time.
        </Paragraph>
      </div>
    ),
  },
  {
    title: 'Your Knowledge Map',
    icon: <NodeIndexOutlined />,
    content: (
      <div style={{ textAlign: 'center', padding: '24px 0' }}>
        <Title level={4}>Track Your Progress</Title>
        <Paragraph>
          The Knowledge Map visualizes your mastery across all programming
          concepts. Watch your skills grow as you solve problems — the system
          tracks your progress through Bayesian Knowledge Tracing and spaced
          repetition scheduling.
        </Paragraph>
      </div>
    ),
  },
  {
    title: 'Get Started',
    icon: <TrophyOutlined />,
    content: (
      <div style={{ textAlign: 'center', padding: '24px 0' }}>
        <Title level={4}>Ready to Learn?</Title>
        <Paragraph>
          Head to the Dashboard to see your personalized recommendations, or
          browse the Problem list to start solving. The system learns from
          every submission to give you better suggestions over time.
        </Paragraph>
      </div>
    ),
  },
];

function OnboardingModal() {
  const [open, setOpen] = useState(false);
  const [current, setCurrent] = useState(0);
  const navigate = useNavigate();

  useEffect(() => {
    const done = localStorage.getItem(ONBOARDING_KEY);
    if (!done) {
      setOpen(true);
    }
  }, []);

  const handleClose = () => {
    localStorage.setItem(ONBOARDING_KEY, 'true');
    setOpen(false);
  };

  const handleFinish = () => {
    handleClose();
    navigate('/problems');
  };

  const isLast = current === steps.length - 1;

  return (
    <Modal
      open={open}
      onCancel={handleClose}
      footer={null}
      width={560}
      closable
    >
      <Steps
        current={current}
        items={steps.map((s) => ({ title: s.title, icon: s.icon }))}
        size="small"
        style={{ marginBottom: 24 }}
      />

      {steps[current]?.content}

      <div style={{ textAlign: 'right', marginTop: 16 }}>
        <Space>
          {current > 0 && (
            <Button onClick={() => setCurrent(current - 1)}>Previous</Button>
          )}
          {isLast ? (
            <Button type="primary" onClick={handleFinish}>
              Start Learning
            </Button>
          ) : (
            <Button type="primary" onClick={() => setCurrent(current + 1)}>
              Next
            </Button>
          )}
        </Space>
      </div>
    </Modal>
  );
}

export default OnboardingModal;
