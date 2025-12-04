'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { logger } from '@/lib/logger';

interface ResourceStatus {
  database: {
    size_mb: number;
    limit_mb: number;
    percentage_used: number;
    status: string;
  };
  redis: {
    commands_today: number;
    limit_per_day: number;
    percentage_used: number;
    status: string;
  };
  storage: {
    size_gb: number;
    cost_estimate_usd: number;
    status: string;
  };
  timestamp: string;
}

interface Alert {
  resource: string;
  level: string;
  message: string;
  current: number;
  limit: number;
  percentage: number;
  timestamp: string;
}

export default function ResourceMonitor() {
  const [status, setStatus] = useState<ResourceStatus | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadMonitoringData();
    // Refresh every 5 minutes
    const interval = setInterval(loadMonitoringData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const loadMonitoringData = async () => {
    try {
      setLoading(true);
      const [statusData, alertsData] = await Promise.all([
        api.getMonitoringStatus(),
        api.getMonitoringAlerts()
      ]);
      setStatus(statusData);
      setAlerts(alertsData.alerts);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load monitoring data');
      logger.error('Monitoring error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'critical':
        return 'text-red-600 bg-red-50';
      case 'warning':
        return 'text-yellow-600 bg-yellow-50';
      case 'ok':
        return 'text-green-600 bg-green-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getProgressColor = (percentage: number) => {
    if (percentage >= 95) return 'bg-red-500';
    if (percentage >= 80) return 'bg-yellow-500';
    return 'bg-green-500';
  };

  if (loading && !status) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Resource Monitoring</h2>
        <p className="text-gray-500">Loading...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">Resource Monitoring</h2>
        <p className="text-red-500">Error: {error}</p>
      </div>
    );
  }

  if (!status) return null;

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold">Resource Monitoring</h2>
        <button
          onClick={loadMonitoringData}
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          Refresh
        </button>
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <div className="mb-6 space-y-2">
          {alerts.map((alert, idx) => (
            <div
              key={idx}
              className={`p-3 rounded ${getStatusColor(alert.level)}`}
            >
              <div className="font-semibold">{alert.resource.toUpperCase()}</div>
              <div className="text-sm">{alert.message}</div>
            </div>
          ))}
        </div>
      )}

      {/* Database */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <h3 className="font-semibold">Database (PostgreSQL)</h3>
          <span className={`px-2 py-1 rounded text-sm ${getStatusColor(status.database.status)}`}>
            {status.database.status.toUpperCase()}
          </span>
        </div>
        <div className="text-sm text-gray-600 mb-2">
          {status.database.size_mb.toFixed(1)} MB / {status.database.limit_mb} MB
          ({status.database.percentage_used.toFixed(1)}%)
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full ${getProgressColor(status.database.percentage_used)}`}
            style={{ width: `${Math.min(status.database.percentage_used, 100)}%` }}
          />
        </div>
      </div>

      {/* Redis */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <h3 className="font-semibold">Redis (Commands Today)</h3>
          <span className={`px-2 py-1 rounded text-sm ${getStatusColor(status.redis.status)}`}>
            {status.redis.status.toUpperCase()}
          </span>
        </div>
        <div className="text-sm text-gray-600 mb-2">
          {status.redis.commands_today.toLocaleString()} / {status.redis.limit_per_day.toLocaleString()} commands
          ({status.redis.percentage_used.toFixed(1)}%)
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className={`h-2 rounded-full ${getProgressColor(status.redis.percentage_used)}`}
            style={{ width: `${Math.min(status.redis.percentage_used, 100)}%` }}
          />
        </div>
      </div>

      {/* Storage */}
      <div>
        <div className="flex justify-between items-center mb-2">
          <h3 className="font-semibold">Storage (BunnyCDN)</h3>
          <span className={`px-2 py-1 rounded text-sm ${getStatusColor(status.storage.status)}`}>
            {status.storage.status.toUpperCase()}
          </span>
        </div>
        <div className="text-sm text-gray-600">
          {status.storage.size_gb.toFixed(2)} GB
        </div>
        <div className="text-sm text-gray-600 mt-1">
          Estimated cost: ${status.storage.cost_estimate_usd.toFixed(2)}/month
        </div>
      </div>

      {status.timestamp && (
        <div className="mt-4 text-xs text-gray-500">
          Last updated: {new Date(status.timestamp).toLocaleString()}
        </div>
      )}
    </div>
  );
}

