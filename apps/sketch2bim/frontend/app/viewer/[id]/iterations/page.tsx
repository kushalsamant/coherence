import { auth } from '@/auth';
import { redirect } from 'next/navigation';
import { api } from '@/lib/api';
import IterationCompare from '@/components/IterationCompare';
import Link from 'next/link';

interface PageProps {
  params: {
    id: string;
  };
  searchParams: {
    compare?: string;
    iteration1?: string;
    iteration2?: string;
  };
}

export default async function IterationsPage({ params, searchParams }: PageProps) {
  const session = await auth();
  
  if (!session) {
    redirect('/api/auth/signin');
  }

  const jobId = params.id;
  const { compare, iteration1, iteration2 } = searchParams;

  // If compare mode, show comparison view
  if (compare === 'true') {
    return (
      <div className="h-screen">
        <IterationCompare 
          jobId={jobId} 
          iteration1Id={iteration1}
          iteration2Id={iteration2}
        />
      </div>
    );
  }

  // Otherwise show iterations list
  let iterations: any[] = [];
  try {
    iterations = await api.listIterations(jobId);
  } catch (error) {
    if (process.env.NODE_ENV === 'development') {
      console.error('Failed to load iterations');
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <Link 
            href={`/viewer/${jobId}`}
            className="text-primary-600 dark:text-primary-400 hover:text-primary-700 mb-4 inline-block"
          >
            ← Back to Viewer
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">Iterations</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            View and compare different versions of your IFC model
          </p>
        </div>

        {/* Iterations List */}
        {iterations.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-12 text-center">
            <svg className="mx-auto h-12 w-12 text-gray-400 dark:text-gray-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">No iterations yet</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Create your first iteration by editing the IFC model in the viewer
            </p>
            <Link
              href={`/viewer/${jobId}`}
              className="inline-block px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              Go to Viewer
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {iterations.map((iteration, index) => (
              <div
                key={iteration.id}
                className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                        {iteration.name || `Iteration ${index + 1}`}
                      </h3>
                      {iteration.change_summary && (
                        <span className="text-xs px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 rounded">
                          {iteration.change_summary}
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">
                      Created {new Date(iteration.created_at).toLocaleString()}
                    </p>
                    {iteration.notes && (
                      <p className="text-sm text-gray-700 dark:text-gray-300 mb-3">{iteration.notes}</p>
                    )}
                  </div>
                  <div className="flex gap-2">
                    {iteration.ifc_url && (
                      <>
                        <Link
                          href={`/viewer/${jobId}?iteration=${iteration.id}`}
                          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm"
                        >
                          View
                        </Link>
                        <Link
                          href={`/viewer/${jobId}/iterations?compare=true&iteration1=${iteration.id}&iteration2=original`}
                          className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors text-sm"
                        >
                          Compare
                        </Link>
                      </>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

