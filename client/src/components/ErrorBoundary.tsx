import { Component, type ErrorInfo, type ReactNode } from 'react';
import { Button, Result } from 'antd';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }
      return (
        <Result
          status="error"
          title="Something went wrong"
          subTitle={this.state.error?.message || 'An unexpected error occurred. Please try again.'}
          extra={[
            <Button type="primary" key="retry" onClick={this.handleReset}>
              Try Again
            </Button>,
            <Button key="home" onClick={() => (window.location.href = '/')}>
              Go Home
            </Button>,
          ]}
        />
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
