import { useState } from 'react';
import { Modal, Steps, Typography, Button, Space } from 'antd';
import {
  RocketOutlined,
  ExperimentOutlined,
  DashboardOutlined,
  CodeOutlined,
  QuestionCircleOutlined,
  NodeIndexOutlined,
  CalendarOutlined,
  BulbOutlined,
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useOnboarding } from '../../hooks/useOnboarding';
import { useResponsive } from '../../hooks/useResponsive';
import styles from './WelcomeFlow.module.css';

const { Title, Paragraph, Text } = Typography;

function WelcomeFlow() {
  const { state, completeWelcome } = useOnboarding();
  const [current, setCurrent] = useState(0);
  const navigate = useNavigate();
  const { isMobile } = useResponsive();

  if (state.welcomeDone) return null;

  const steps = [
    {
      title: 'Welcome',
      icon: <RocketOutlined />,
      content: (
        <div className={styles.stepContent}>
          <Title level={4}>Welcome to AdaptLearn!</Title>
          <Paragraph>
            AdaptLearn is your personalized programming learning companion.
            It adapts to your skill level in real-time, picking the right
            problems at the right time to maximize your learning.
          </Paragraph>
          <Paragraph type="secondary">
            Let us show you around — this will only take a minute.
          </Paragraph>
        </div>
      ),
    },
    {
      title: 'How It Works',
      icon: <ExperimentOutlined />,
      content: (
        <div className={styles.stepContent}>
          <Title level={4}>Smart Learning, Made Simple</Title>
          <Paragraph>
            Behind the scenes, AdaptLearn uses AI to understand what you know
            and what you need to practice. Here is what it does for you:
          </Paragraph>
          <div className={styles.featureGrid}>
            <div className={styles.featureItem}>
              <BulbOutlined />
              <div>
                <Text strong>Tracks your mastery</Text>
                <br />
                <Text type="secondary">Knows which concepts you have nailed</Text>
              </div>
            </div>
            <div className={styles.featureItem}>
              <ExperimentOutlined />
              <div>
                <Text strong>Picks the right challenge</Text>
                <br />
                <Text type="secondary">Not too easy, not too hard</Text>
              </div>
            </div>
            <div className={styles.featureItem}>
              <CalendarOutlined />
              <div>
                <Text strong>Schedules reviews</Text>
                <br />
                <Text type="secondary">Reminds you before you forget</Text>
              </div>
            </div>
            <div className={styles.featureItem}>
              <NodeIndexOutlined />
              <div>
                <Text strong>Maps your knowledge</Text>
                <br />
                <Text type="secondary">Visualizes your learning journey</Text>
              </div>
            </div>
          </div>
        </div>
      ),
    },
    {
      title: 'Dashboard',
      icon: <DashboardOutlined />,
      content: (
        <div className={styles.stepContent}>
          <Title level={4}>Your Home Base</Title>
          <Paragraph>
            The Dashboard shows your stats, recommended problems, and recent
            activity. Everything updates automatically as you solve problems.
          </Paragraph>
          <Paragraph type="secondary">
            It might look empty at first — that is normal! It fills up as you
            start solving.
          </Paragraph>
        </div>
      ),
    },
    {
      title: 'First Problem',
      icon: <CodeOutlined />,
      content: (
        <div className={styles.stepContent}>
          <Title level={4}>Ready to Start?</Title>
          <Paragraph>
            The best way to learn is to jump in. We will take you to the
            problem list where you can pick an easy problem to begin.
          </Paragraph>
          <Paragraph type="secondary">
            Do not worry about getting it wrong — the system learns from every
            attempt and adjusts to help you improve!
          </Paragraph>
        </div>
      ),
    },
    {
      title: 'Get Help',
      icon: <QuestionCircleOutlined />,
      content: (
        <div className={styles.stepContent}>
          <Title level={4}>Help Is Always Available</Title>
          <Paragraph>
            Each page has a guided tour that explains its features. You can
            replay any tour anytime.
          </Paragraph>
          <div className={styles.helpTip}>
            <QuestionCircleOutlined style={{ fontSize: 20, color: '#1677ff' }} />
            <Text>
              Look for the <Text strong>?</Text> icon in the top-right corner
              to access tours, terminology glossary, and more.
            </Text>
          </div>
        </div>
      ),
    },
  ];

  const isLast = current === steps.length - 1;

  const handleClose = () => {
    completeWelcome();
  };

  const handleFinish = () => {
    completeWelcome();
    navigate('/problems?difficulty=EASY');
  };

  return (
    <Modal
      open
      onCancel={handleClose}
      footer={null}
      width={isMobile ? '100%' : 600}
      closable
    >
      {isMobile ? (
        <div className={styles.stepIndicator}>
          <Text type="secondary">
            Step {current + 1} of {steps.length}
          </Text>
        </div>
      ) : (
        <Steps
          current={current}
          items={steps.map((s) => ({ title: s.title, icon: s.icon }))}
          size="small"
          style={{ marginBottom: 24 }}
        />
      )}

      {steps[current]?.content}

      <div className={styles.footer}>
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

export default WelcomeFlow;
