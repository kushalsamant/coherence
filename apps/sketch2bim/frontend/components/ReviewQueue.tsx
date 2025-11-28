'use client';

import { useEffect, useState } from 'react';
import { api, Job } from '@/lib/api';
import JobCard from './JobCard';

export default function ReviewQueue() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReviewJobs();
    const interval = setInterval(loadReviewJobs, 10000); // Poll every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const loadReviewJobs = async () => {
    try {
      const allJobs = await api.listJobs();
      const reviewJobs = allJobs.filter(job => job.status === 'review');
      setJobs(reviewJobs);
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to load review jobs');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (jobId: string) => {
    try {
      await api.deleteJob(jobId);
      setJobs(jobs.filter(job => job.id !== jobId));
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to delete job');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="card text-center py-8 bg-green-50 border-green-200">
        <div className="text-4xl mb-2">✓</div>
        <h3 className="text-lg font-semibold text-green-800 mb-1">
          No jobs require review
        </h3>
        <p className="text-sm text-green-600">
          All jobs are approved or processing
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">
          Review Queue ({jobs.length})
        </h2>
        <p className="text-sm text-gray-600">
          Jobs with low confidence scores require manual review
        </p>
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

