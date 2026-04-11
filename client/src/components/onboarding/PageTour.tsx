import { Tour } from 'antd';
import type { TourProps } from 'antd';
import { useEffect, useState } from 'react';
import { useOnboarding } from '../../hooks/useOnboarding';
import type { OnboardingState } from '../../contexts/OnboardingContext';

type TourKey = keyof OnboardingState['tours'];

interface PageTourProps {
  tourKey: TourKey;
  steps: TourProps['steps'];
  autoOpen?: boolean;
}

export default function PageTour({ tourKey, steps, autoOpen = true }: PageTourProps) {
  const { shouldShowTour, completeTour } = useOnboarding();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (autoOpen && shouldShowTour(tourKey)) {
      // Delay so page content renders and refs attach
      const timer = setTimeout(() => setOpen(true), 600);
      return () => clearTimeout(timer);
    }
  }, [autoOpen, shouldShowTour, tourKey]);

  const handleClose = () => {
    setOpen(false);
    completeTour(tourKey);
  };

  return (
    <Tour
      open={open}
      onClose={handleClose}
      onFinish={handleClose}
      steps={steps}
    />
  );
}
