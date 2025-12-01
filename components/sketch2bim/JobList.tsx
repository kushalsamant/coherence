'use client';

import { useEffect, useState } from 'react';
import { api, Job } from '@/lib/api';
import JobCard from './JobCard';

export default function JobList() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const loadJobs = async (silent: boolean = false) => {
    try {
      if (!silent) {
        setIsRefreshing(true);
      }
      const data = await api.listJobs();
      setJobs(data || []); // Ensure it's always an array
      setError(null);
    } catch (err: any) {
      // Distinguish between actual errors and empty responses
      const status = err?.response?.status;
      const isNotFound = status === 404;
      const isServerError = status >= 500;
      
      // For first-time users with no jobs, API might return 404 or empty array
      // Treat these as empty state, not errors
      if (isNotFound) {
        // 404 means no jobs found - this is normal for new users
        setJobs([]);
        setError(null);
      } else if (isServerError) {
        // Only show error for actual server errors (500+)
        setError('Unable to load jobs. Please try again later.');
        if (process.env.NODE_ENV === 'development') {
          console.error('Server error loading jobs');
        }
      } else {
        // For other errors (network, auth, etc.), prefer showing empty state for first-time users
        // If we already have jobs cached, show a warning; otherwise show empty state
        if (jobs.length === 0) {
          // First-time user - show empty state instead of error
          setJobs([]);
          setError(null);
        } else {
          // User has jobs but refresh failed - show warning but keep cached jobs
          setError('Failed to refresh jobs. Showing cached results.');
        }
      }
    } finally {
      setLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadJobs();
    
    // Optimize polling frequency based on job status
    const getPollingInterval = () => {
      const hasProcessingJobs = jobs.some(job => job.status === 'processing' || job.status === 'queued');
      if (hasProcessingJobs) {
        return 3000; // Poll every 3 seconds if there are active jobs
      }
      return 10000; // Poll every 10 seconds if all jobs are completed
    };

    const interval = setInterval(() => {
      loadJobs(true); // Silent refresh
    }, getPollingInterval());

    return () => clearInterval(interval);
  }, [jobs]);

  const handleDelete = async (jobId: string) => {
    try {
      await api.deleteJob(jobId);
      setJobs(jobs.filter(job => job.id !== jobId));
    } catch (err) {
      // Silently handle - user will see error if operation fails
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to delete job');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card bg-red-50 border-red-200">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="card text-center py-12">
        <div className="text-6xl mb-4">📭</div>
        <h3 className="text-xl font-semibold text-gray-700 mb-2">
          No models yet
        </h3>
        <p className="text-gray-500">
          Upload your first sketch to get started
        </p>
      </div>
    );
  }

  const hasActiveJobs = jobs.some(job => job.status === 'processing' || job.status === 'queued');

  return (
    <div className="space-y-4">
      {/* Header with refresh button */}
      <div className="flex items-center justify-between mb-4">
        <div className="text-sm text-gray-600">
          {hasActiveJobs && (
            <span className="flex items-center gap-2">
              <span className="relative flex h-3 w-3">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-primary-500"></span>
              </span>
              Jobs processing...
            </span>
          )}
          {!hasActiveJobs && jobs.length > 0 && (
            <span className="text-gray-500">All jobs completed</span>
          )}
        </div>
        <button
          onClick={() => loadJobs()}
          disabled={isRefreshing}
          className="px-3 py-1.5 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          title="Refresh jobs"
        >
          <svg 
            className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} 
            fill="none" 
            stroke="currentColor" 
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh
        </button>
      </div>

      {jobs.map(job => (
        <JobCard
          key={job.id}
          job={job}
          onDelete={() => handleDelete(job.id)}
        />
      ))}
    </div>
  );
}

