import { Alert, Button } from 'antd';
import { useNavigate } from 'react-router-dom';
import { RocketOutlined } from '@ant-design/icons';

interface ColdStartBannerProps {
  problemsSolved: number;
}

export default function ColdStartBanner({ problemsSolved }: ColdStartBannerProps) {
  const navigate = useNavigate();

  if (problemsSolved > 0) return null;

  return (
    <Alert
      type="info"
      banner
      showIcon
      icon={<RocketOutlined />}
      message="Welcome! Start by solving your first problem to unlock personalized recommendations, your Knowledge Map, and review scheduling."
      action={
        <Button size="small" type="primary" onClick={() => navigate('/problems?difficulty=EASY')}>
          Solve Your First Problem
        </Button>
      }
      style={{ marginBottom: 16, borderRadius: 6 }}
    />
  );
}
