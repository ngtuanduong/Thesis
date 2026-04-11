import { Dropdown } from 'antd';
import type { MenuProps } from 'antd';
import {
  QuestionCircleOutlined,
  ReloadOutlined,
  BookOutlined,
  ClearOutlined,
} from '@ant-design/icons';
import { useLocation, useNavigate } from 'react-router-dom';
import { useOnboarding } from '../../hooks/useOnboarding';
import type { OnboardingState } from '../../contexts/OnboardingContext';

type TourKey = keyof OnboardingState['tours'];

const routeToTourKey: Record<string, TourKey> = {
  '/': 'dashboard',
  '/problems': 'problems',
  '/knowledge-map': 'knowledgeMap',
  '/review-queue': 'reviewQueue',
};

const tourLabels: Record<TourKey, string> = {
  dashboard: 'Dashboard',
  problems: 'Problems',
  problemDetail: 'Problem Detail',
  knowledgeMap: 'Knowledge Map',
  reviewQueue: 'Review Queue',
};

export default function HelpMenu() {
  const { restartTour, resetAll } = useOnboarding();
  const location = useLocation();
  const navigate = useNavigate();

  const currentTourKey = location.pathname.startsWith('/problems/')
    ? 'problemDetail' as TourKey
    : routeToTourKey[location.pathname];

  const items: MenuProps['items'] = [
    ...(currentTourKey
      ? [
          {
            key: 'replay-current',
            icon: <ReloadOutlined />,
            label: `Replay ${tourLabels[currentTourKey]} Tour`,
            onClick: () => restartTour(currentTourKey),
          },
        ]
      : []),
    {
      key: 'glossary',
      icon: <BookOutlined />,
      label: 'Terminology Glossary',
      onClick: () => navigate('/glossary'),
    },
    { type: 'divider' },
    {
      key: 'reset',
      icon: <ClearOutlined />,
      label: 'Reset All Tours',
      onClick: resetAll,
    },
  ];

  return (
    <Dropdown menu={{ items }} placement="bottomRight" trigger={['click']}>
      <QuestionCircleOutlined
        style={{ fontSize: 18, cursor: 'pointer', color: '#595959' }}
      />
    </Dropdown>
  );
}
