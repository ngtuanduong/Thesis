import { ConfigProvider, App as AntApp } from 'antd';
import AppRoutes from './routes';
import { OnboardingProvider } from './contexts/OnboardingContext';

function App() {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1677ff',
          borderRadius: 6,
        },
      }}
    >
      <AntApp>
        <OnboardingProvider>
          <AppRoutes />
        </OnboardingProvider>
      </AntApp>
    </ConfigProvider>
  );
}

export default App;
