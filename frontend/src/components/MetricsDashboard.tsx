import { useQuery } from '@tanstack/react-query';
import { FileText, MessageSquare, Clock, TrendingUp } from 'lucide-react';
import { api } from '../services/api';

export default function MetricsDashboard() {
  const { data: metrics, isLoading } = useQuery({
    queryKey: ['metrics'],
    queryFn: api.getMetrics,
    refetchInterval: 5000,
  });

  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: api.getHealth,
    refetchInterval: 10000,
  });

  const stats = [
    {
      label: 'Total Documents',
      value: metrics?.total_documents || 0,
      icon: FileText,
      color: 'bg-blue-500',
    },
    {
      label: 'Total Chunks',
      value: metrics?.total_chunks || 0,
      icon: FileText,
      color: 'bg-purple-500',
    },
    {
      label: 'Total Queries',
      value: metrics?.total_queries || 0,
      icon: MessageSquare,
      color: 'bg-green-500',
    },
    {
      label: 'Avg Response Time',
      value: `${(metrics?.avg_response_time || 0).toFixed(2)}s`,
      icon: Clock,
      color: 'bg-orange-500',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-effect rounded-2xl p-8">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-800 mb-2">
              System Metrics
            </h2>
            <p className="text-slate-600">
              Real-time performance and usage statistics
            </p>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-green-50 rounded-full">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm font-medium text-green-700">
              {health?.status || 'Unknown'}
            </span>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div
              key={stat.label}
              className="glass-effect rounded-2xl p-6 hover:shadow-xl transition-shadow"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 ${stat.color} rounded-xl flex items-center justify-center`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <TrendingUp className="w-5 h-5 text-green-500" />
              </div>
              <p className="text-3xl font-bold text-slate-800 mb-1">
                {isLoading ? '...' : stat.value}
              </p>
              <p className="text-sm text-slate-600">{stat.label}</p>
            </div>
          );
        })}
      </div>

      {/* Services Status */}
      <div className="glass-effect rounded-2xl p-8">
        <h3 className="text-xl font-bold text-slate-800 mb-4">
          Services Status
        </h3>
        <div className="space-y-3">
          {health?.services &&
            Object.entries(health.services).map(([service, status]) => (
              <div
                key={service}
                className="flex items-center justify-between p-4 bg-white border border-slate-200 rounded-xl"
              >
                <span className="font-medium text-slate-800 capitalize">
                  {service}
                </span>
                <div
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    status
                      ? 'bg-green-100 text-green-700'
                      : 'bg-red-100 text-red-700'
                  }`}
                >
                  {status ? 'Healthy' : 'Down'}
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}
