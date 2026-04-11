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
  const { state, shouldShowTour, completeTour } = useOnboarding();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    // Don't open tour while the welcome modal is still showing
    if (autoOpen && state.welcomeDone && shouldShowTour(tourKey)) {
      // Delay so page content renders and refs attach
      const timer = setTimeout(() => setOpen(true), 600);
      return () => clearTimeout(timer);
    }
  }, [autoOpen, state.welcomeDone, shouldShowTour, tourKey]);

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
