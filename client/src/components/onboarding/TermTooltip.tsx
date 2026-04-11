import { Tooltip } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import type { ReactNode } from 'react';
import { GLOSSARY } from './glossary';

interface TermTooltipProps {
  term: string;
  children: ReactNode;
}

export default function TermTooltip({ term, children }: TermTooltipProps) {
  const entry = GLOSSARY[term];
  if (!entry) return <>{children}</>;

  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
      {children}
      <Tooltip title={<span><strong>{entry.short}</strong><br />{entry.detail}</span>}>
        <InfoCircleOutlined style={{ fontSize: 12, color: '#8c8c8c', cursor: 'help' }} />
      </Tooltip>
    </span>
  );
}
