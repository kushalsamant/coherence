'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

export default function UsageStats() {
  const [stats, setStats] = useState<{
    totalJobs: number;
    completedJobs: number;
    failedJobs: number;
    thisMonth: number;
  } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const jobs = await api.listJobs(100, 0);
      
      const now = new Date();
      const startOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
      
      const thisMonthJobs = jobs.filter(job => {
        const jobDate = new Date(job.created_at);
        return jobDate >= startOfMonth;
      });

      setStats({
        totalJobs: jobs.length,
        completedJobs: jobs.filter(j => j.status === 'completed').length,
        failedJobs: jobs.filter(j => j.status === 'failed').length,
        thisMonth: thisMonthJobs.length
      });
    } catch (error) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to load stats');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/3"></div>
          <div className="grid grid-cols-2 gap-4">
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  const successRate = stats.totalJobs > 0 
    ? Math.round((stats.completedJobs / stats.totalJobs) * 100) 
    : 0;

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Usage Statistics</h3>
      
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Total Jobs */}
        <div className="bg-gray-50 rounded-lg p-4">
          <p className="text-sm text-gray-600 mb-1">Total Jobs</p>
          <p className="text-2xl font-bold text-gray-900">{stats.totalJobs}</p>
        </div>

        {/* This Month */}
        <div className="bg-blue-50 rounded-lg p-4">
          <p className="text-sm text-blue-600 mb-1">This Month</p>
          <p className="text-2xl font-bold text-blue-900">{stats.thisMonth}</p>
        </div>

        {/* Completed */}
        <div className="bg-green-50 rounded-lg p-4">
          <p className="text-sm text-green-600 mb-1">Completed</p>
          <p className="text-2xl font-bold text-green-900">{stats.completedJobs}</p>
        </div>

        {/* Success Rate */}
        <div className="bg-purple-50 rounded-lg p-4">
          <p className="text-sm text-purple-600 mb-1">Success Rate</p>
          <p className="text-2xl font-bold text-purple-900">{successRate}%</p>
        </div>
      </div>

      {/* Simple Chart */}
      {stats.totalJobs > 0 && (
        <div className="mt-6">
          <div className="flex items-center gap-2 mb-2">
            <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-green-500 transition-all duration-300"
                style={{ width: `${(stats.completedJobs / stats.totalJobs) * 100}%` }}
              ></div>
            </div>
            <span className="text-xs text-gray-600">
              {stats.completedJobs}/{stats.totalJobs}
            </span>
          </div>
          <p className="text-xs text-gray-500 text-center">
            {stats.completedJobs} completed, {stats.failedJobs} failed
          </p>
        </div>
      )}
    </div>
  );
}

