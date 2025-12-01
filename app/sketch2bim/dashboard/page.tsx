import { redirect } from 'next/navigation';
import Link from 'next/link';
import { auth } from '@/app/sketch2bim/auth';
import UploadForm from '@/components/sketch2bim/UploadForm';
import JobList from '@/components/sketch2bim/JobList';
import ReviewQueue from '@/components/sketch2bim/ReviewQueue';
import CreditsDisplay from '@/components/sketch2bim/CreditsDisplay';
import UsageStats from '@/components/sketch2bim/UsageStats';

export default async function Dashboard() {
  const session = await auth();

  if (!session) {
    redirect('/api/auth/signin');
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Upload Section */}
          <div className="lg:col-span-1">
            <div className="card sticky top-8">
              <h2 className="text-xl font-semibold mb-4">Upload Sketch</h2>
              <UploadForm />
            </div>
          </div>

          {/* Jobs Section */}
          <div className="lg:col-span-2 space-y-8">
            {/* Usage Stats */}
            <UsageStats />

            {/* Review Queue */}
            <div>
              <h2 className="text-2xl font-semibold mb-4">Review Queue</h2>
              <ReviewQueue />
            </div>

            {/* All Jobs */}
            <div>
              <h2 className="text-2xl font-semibold mb-4">Your Models</h2>
              <JobList />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

