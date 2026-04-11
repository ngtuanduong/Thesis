import { useState } from 'react';
import { Dropdown, Modal, Typography } from 'antd';
import type { MenuProps } from 'antd';
import {
  QuestionCircleOutlined,
  ReloadOutlined,
  BookOutlined,
  ClearOutlined,
} from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import { useOnboarding } from '../../hooks/useOnboarding';
import { GLOSSARY } from './glossary';
import type { OnboardingState } from '../../contexts/OnboardingContext';

const { Title, Paragraph, Text } = Typography;

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
  const [glossaryOpen, setGlossaryOpen] = useState(false);

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
      onClick: () => setGlossaryOpen(true),
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
    <>
      <Dropdown menu={{ items }} placement="bottomRight" trigger={['click']}>
        <QuestionCircleOutlined
          style={{ fontSize: 18, cursor: 'pointer', color: '#595959' }}
        />
      </Dropdown>

      <Modal
        title="Terminology Glossary"
        open={glossaryOpen}
        onCancel={() => setGlossaryOpen(false)}
        footer={null}
        width={560}
      >
        {Object.entries(GLOSSARY).map(([key, entry]) => (
          <div key={key} style={{ marginBottom: 16 }}>
            <Title level={5} style={{ marginBottom: 4, textTransform: 'capitalize' }}>
              {key.replace(/_/g, ' ')}
            </Title>
            <Text strong>{entry.short}</Text>
            <Paragraph type="secondary" style={{ marginBottom: 0, marginTop: 4 }}>
              {entry.detail}
            </Paragraph>
          </div>
        ))}
      </Modal>
    </>
  );
}
