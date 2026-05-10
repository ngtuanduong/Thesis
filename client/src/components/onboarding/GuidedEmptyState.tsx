import { Empty, Button } from 'antd';
import { useNavigate } from 'react-router-dom';
import {
  RocketOutlined,
  ExperimentOutlined,
  NodeIndexOutlined,
  HistoryOutlined,
} from '@ant-design/icons';

type EmptyType = 'recommendations' | 'activity' | 'knowledge' | 'reviews';

interface GuidedEmptyStateProps {
  type: EmptyType;
}

const configs: Record<EmptyType, { icon: React.ReactNode; message: string; cta: string; link: string }> = {
  recommendations: {
    icon: <ExperimentOutlined style={{ fontSize: 48, color: '#bfbfbf' }} />,
    message:
      'The adaptive engine needs to see you solve a few problems before it can make personalized recommendations. Start with an easy problem to get going!',
    cta: 'Browse Easy Problems',
    link: '/problems?difficulty=EASY',
  },
  activity: {
    icon: <HistoryOutlined style={{ fontSize: 48, color: '#bfbfbf' }} />,
    message:
      'Your activity will appear here once you start solving problems. Each submission helps the system learn about your strengths and areas to improve.',
    cta: 'Start Solving',
    link: '/problems',
  },
  knowledge: {
    icon: <NodeIndexOutlined style={{ fontSize: 48, color: '#bfbfbf' }} />,
    message:
      'Your knowledge map builds as you solve problems. Each submission updates your mastery across related concepts — solve your first problem to see it grow!',
    cta: 'Solve Your First Problem',
    link: '/problems?difficulty=EASY',
  },
  reviews: {
    icon: <RocketOutlined style={{ fontSize: 48, color: '#bfbfbf' }} />,
    message:
      'Once you master some concepts, the system will schedule reviews at optimal times to help you retain what you have learned. Keep solving to unlock reviews!',
    cta: 'Keep Learning',
    link: '/problems',
  },
};

export default function GuidedEmptyState({ type }: GuidedEmptyStateProps) {
  const navigate = useNavigate();
  const config = configs[type];

  return (
    <Empty
      image={config.icon}
      imageStyle={{ height: 60 }}
      description={<span style={{ color: '#595959', maxWidth: 400, display: 'inline-block' }}>{config.message}</span>}
    >
      <Button type="primary" onClick={() => navigate(config.link)}>
        {config.cta}
      </Button>
    </Empty>
  );
}
