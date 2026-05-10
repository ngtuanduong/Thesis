import { Tooltip } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';
import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
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
      <Tooltip title={
        <span>
          <strong>{entry.short}</strong>
          <br />
          {entry.detail}
          <br />
          <Link
            to={`/glossary#${term}`}
            style={{ fontSize: 11, color: '#69b1ff' }}
            onClick={(e) => e.stopPropagation()}
          >
            Learn more &rarr;
          </Link>
        </span>
      }>
        <InfoCircleOutlined style={{ fontSize: 12, color: '#8c8c8c', cursor: 'help' }} />
      </Tooltip>
    </span>
  );
}
