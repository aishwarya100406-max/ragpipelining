import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useState } from 'react';
import Header from './components/Header';
import ChatInterface from './components/ChatInterface';
import DocumentUpload from './components/DocumentUpload';
import Sidebar from './components/Sidebar';
import MetricsDashboard from './components/MetricsDashboard';

const queryClient = new QueryClient();

type View = 'chat' | 'upload' | 'metrics';

function App() {
  const [currentView, setCurrentView] = useState<View>('chat');

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen flex flex-col">
        <Header />
        
        <div className="flex-1 flex">
          <Sidebar currentView={currentView} onViewChange={setCurrentView} />
          
          <main className="flex-1 p-6">
            {currentView === 'chat' && <ChatInterface />}
            {currentView === 'upload' && <DocumentUpload />}
            {currentView === 'metrics' && <MetricsDashboard />}
          </main>
        </div>
      </div>
    </QueryClientProvider>
  );
}

export default App;
