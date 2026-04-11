import type { ReactNode } from 'react';
import { Tooltip } from 'antd';
import { InfoCircleOutlined } from '@ant-design/icons';

/**
 * Strategy B: For non-sortable columns that need a description.
 * Renders "Title (i)" where the icon shows a tooltip on hover.
 */
export function columnTitle(title: string, tooltip: string): ReactNode {
  return (
    <span style={{ display: 'inline-flex', alignItems: 'center', gap: 4 }}>
      {title}
      <Tooltip title={tooltip}>
        <InfoCircleOutlined style={{ fontSize: 11, color: '#bfbfbf', cursor: 'help' }} />
      </Tooltip>
    </span>
  );
}

/**
 * Strategy A: For sortable columns that need a description.
 * Returns a showSorterTooltip config that replaces the default sort tooltip.
 */
export function sorterTooltip(tooltip: string): { title: string } {
  return { title: tooltip };
}
