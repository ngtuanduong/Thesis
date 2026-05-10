import { Grid } from 'antd';

const { useBreakpoint } = Grid;

export function useResponsive() {
  const screens = useBreakpoint();

  return {
    /** < 768px — phones */
    isMobile: !screens.md,
    /** 768px - 991px — tablets */
    isTablet: !!screens.md && !screens.lg,
    /** >= 992px — desktops */
    isDesktop: !!screens.lg,
    breakpoints: screens,
  };
}
