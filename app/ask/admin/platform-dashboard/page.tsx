'use client';

import { Card } from '@kushalsamant/design-template';
import { useRouter } from 'next/navigation';

export default function PlatformDashboard() {
  const router = useRouter();

  return (
    <div className="container mx-auto px-4 py-8">
      <Card className="p-6">
        <div className="text-center space-y-4">
          <h1 className="text-2xl font-bold">Dashboard Moved</h1>
          <p className="text-muted-foreground">
            The platform admin dashboard is now available on the main site.
          </p>
          <p className="text-sm text-muted-foreground">
            Please update your bookmarks to use <code>https://kvshvl.in/admin</code>.
          </p>
          <button
            onClick={() => {
              window.location.href = 'https://kvshvl.in/admin';
            }}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
          >
            Go to New Dashboard
          </button>
          <button
            onClick={() => router.push('/')}
            className="ml-2 px-4 py-2 border rounded-md hover:bg-accent"
          >
            Back to ASK Home
          </button>
        </div>
      </Card>
    </div>
  );
}

