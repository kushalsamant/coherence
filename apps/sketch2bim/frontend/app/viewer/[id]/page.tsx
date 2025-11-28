import { redirect } from 'next/navigation';
import { auth } from '@/auth';
import Link from 'next/link';
import IfcViewer from '@/components/IfcViewer';
import SymbolDetectionPanel from '@/components/SymbolDetectionPanel';

interface ViewerPageProps {
  params: {
    id: string;
  };
}

async function getJob(jobId: string, accessToken: string) {
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  const response = await fetch(`${API_URL}/api/v1/generate/jobs/${jobId}`, {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
    cache: 'no-store',
  });

  if (!response.ok) {
    throw new Error('Failed to fetch job');
  }

  return response.json();
}

export default async function ViewerPage({ params }: ViewerPageProps) {
  const session = await auth();

  if (!session) {
    redirect('/api/auth/signin');
  }

  let job;
  try {
    job = await getJob(params.id, (session as any).accessToken);
  } catch (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">Job not found</h2>
          <Link href="/dashboard" className="btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  if (job.status !== 'completed' || !job.ifc_url) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100 mb-4">
            Model not ready for viewing
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Status: {job.status}
          </p>
          <Link href="/dashboard" className="btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      {/* Header - Mobile responsive */}
      <nav className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 flex-shrink-0">
        <div className="max-w-7xl mx-auto px-2 sm:px-4 lg:px-8">
          <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center py-2 sm:py-0 sm:h-16 gap-2 sm:gap-0">
            <div className="flex items-center gap-2 sm:gap-4 min-w-0">
              <Link 
                href="/dashboard"
                className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 flex-shrink-0 px-2 py-1 sm:px-0 sm:py-0"
              >
                <span className="hidden sm:inline">← Back</span>
                <span className="sm:hidden">←</span>
              </Link>
              <h1 className="text-base sm:text-xl font-semibold text-gray-900 dark:text-gray-100 truncate">
                {job.sketch_filename}
              </h1>
            </div>
            <div className="flex items-center gap-2 sm:gap-3 flex-wrap">
              {job.ifc_url && (
                <a
                  href={job.ifc_url}
                  download
                  className="px-3 sm:px-4 py-1.5 sm:py-2 bg-primary-600 text-white rounded-lg text-xs sm:text-sm hover:bg-primary-700 transition-colors touch-target-lg"
                >
                  <span className="hidden sm:inline">Download IFC</span>
                  <span className="sm:hidden">IFC</span>
                </a>
              )}
              {job.dwg_url && (
                <a
                  href={job.dwg_url}
                  download
                  className="px-3 sm:px-4 py-1.5 sm:py-2 bg-gray-600 text-white rounded-lg text-xs sm:text-sm hover:bg-gray-700 transition-colors touch-target-lg"
                >
                  <span className="hidden sm:inline">Download DWG</span>
                  <span className="sm:hidden">DWG</span>
                </a>
              )}
              {job.symbol_summary && (
                <SymbolDetectionPanel jobId={job.id} summary={job.symbol_summary} buttonVariant="link" />
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Viewer */}
      <div className="flex-1 min-h-0 overflow-hidden">
        <IfcViewer ifc_url={job.ifc_url} />
      </div>
    </div>
  );
}

