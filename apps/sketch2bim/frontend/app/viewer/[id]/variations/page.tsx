import { auth } from '@/auth';
import { redirect } from 'next/navigation';
import LayoutVariations from '@/components/LayoutVariations';
import Link from 'next/link';

interface PageProps {
  params: {
    id: string;
  };
}

export default async function VariationsPage({ params }: PageProps) {
  const session = await auth();
  
  if (!session) {
    redirect('/api/auth/signin');
  }

  const jobId = params.id;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <Link 
            href={`/viewer/${jobId}`}
            className="text-primary-600 hover:text-primary-700 mb-4 inline-block"
          >
            ← Back to Viewer
          </Link>
        </div>

        {/* Variations Component */}
        <LayoutVariations jobId={jobId} />
      </div>
    </div>
  );
}

