import api from '../api/axios';

let sessionId: string | null = null;

function getSessionId(): string {
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
  }
  return sessionId;
}

/**
 * Log a user interaction event to the backend for evaluation/experiment tracking.
 * Fire-and-forget — errors are silently caught.
 */
export function logEvent(event: string, data?: Record<string, unknown>): void {
  const token = localStorage.getItem('token');
  if (!token) return; // not logged in

  api
    .post('/adaptive/log-event', {
      event,
      data: data || {},
      sessionId: getSessionId(),
    })
    .catch(() => {
      // silent — event logging should never break the user experience
    });
}

export function logPageView(page: string): void {
  logEvent('page_view', { page, timestamp: new Date().toISOString() });
}

export function logProblemStart(problemId: string, problemTitle: string): void {
  logEvent('problem_start', { problemId, problemTitle });
}

export function logSubmission(problemId: string, status: string): void {
  logEvent('submission', { problemId, status });
}

export function logHintRequest(problemId: string, hintLevel: number): void {
  logEvent('hint_request', { problemId, hintLevel });
}

export function logRecommendationClick(problemId: string, source: string): void {
  logEvent('recommendation_click', { problemId, source });
}
