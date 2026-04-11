import { createContext, useCallback, useState, useEffect, type ReactNode } from 'react';

const STORAGE_KEY = 'adaptlearn_onboarding';
const OLD_STORAGE_KEY = 'adaptlearn_onboarding_done';

export interface OnboardingState {
  welcomeDone: boolean;
  tours: {
    dashboard: boolean;
    problems: boolean;
    problemDetail: boolean;
    knowledgeMap: boolean;
    reviewQueue: boolean;
  };
  firstProblemSolved: boolean;
  dismissedTerms: string[];
}

type TourKey = keyof OnboardingState['tours'];

export interface OnboardingContextValue {
  state: OnboardingState;
  completeWelcome: () => void;
  completeTour: (key: TourKey) => void;
  restartTour: (key: TourKey) => void;
  resetAll: () => void;
  shouldShowTour: (key: TourKey) => boolean;
  dismissTerm: (term: string) => void;
  markFirstProblemSolved: () => void;
}

const defaultState: OnboardingState = {
  welcomeDone: false,
  tours: {
    dashboard: false,
    problems: false,
    problemDetail: false,
    knowledgeMap: false,
    reviewQueue: false,
  },
  firstProblemSolved: false,
  dismissedTerms: [],
};

function loadState(): OnboardingState {
  try {
    // Migrate from old boolean key
    const oldFlag = localStorage.getItem(OLD_STORAGE_KEY);
    if (oldFlag === 'true') {
      localStorage.removeItem(OLD_STORAGE_KEY);
      const migrated = { ...defaultState, welcomeDone: true };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(migrated));
      return migrated;
    }

    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      return { ...defaultState, ...parsed, tours: { ...defaultState.tours, ...parsed.tours } };
    }
  } catch {
    // ignore parse errors
  }
  return { ...defaultState };
}

function saveState(state: OnboardingState) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

export const OnboardingContext = createContext<OnboardingContextValue>({
  state: defaultState,
  completeWelcome: () => {},
  completeTour: () => {},
  restartTour: () => {},
  resetAll: () => {},
  shouldShowTour: () => false,
  dismissTerm: () => {},
  markFirstProblemSolved: () => {},
});

export function OnboardingProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<OnboardingState>(loadState);

  useEffect(() => {
    saveState(state);
  }, [state]);

  const completeWelcome = useCallback(() => {
    setState((prev) => ({ ...prev, welcomeDone: true }));
  }, []);

  const completeTour = useCallback((key: TourKey) => {
    setState((prev) => ({ ...prev, tours: { ...prev.tours, [key]: true } }));
  }, []);

  const restartTour = useCallback((key: TourKey) => {
    setState((prev) => ({ ...prev, tours: { ...prev.tours, [key]: false } }));
  }, []);

  const resetAll = useCallback(() => {
    setState({ ...defaultState });
  }, []);

  const shouldShowTour = useCallback(
    (key: TourKey) => !state.tours[key],
    [state.tours],
  );

  const dismissTerm = useCallback((term: string) => {
    setState((prev) => ({
      ...prev,
      dismissedTerms: prev.dismissedTerms.includes(term)
        ? prev.dismissedTerms
        : [...prev.dismissedTerms, term],
    }));
  }, []);

  const markFirstProblemSolved = useCallback(() => {
    setState((prev) => ({ ...prev, firstProblemSolved: true }));
  }, []);

  return (
    <OnboardingContext.Provider
      value={{
        state,
        completeWelcome,
        completeTour,
        restartTour,
        resetAll,
        shouldShowTour,
        dismissTerm,
        markFirstProblemSolved,
      }}
    >
      {children}
    </OnboardingContext.Provider>
  );
}
