'use client';

import { useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { trackPageView, trackPageExit } from '@/lib/analytics';

/**
 * Client-side analytics component
 * Tracks page views, navigation flows, and drop-off points
 */
export default function Analytics() {
  const pathname = usePathname();

  useEffect(() => {
    // Track page view on route change
    if (pathname) {
      trackPageView(pathname);
    }

    // Track page exit on unmount or before navigation
    const handleBeforeUnload = () => {
      if (pathname) {
        trackPageExit(pathname);
      }
    };

    // Track visibility change (user switching tabs/windows)
    const handleVisibilityChange = () => {
      if (document.hidden && pathname) {
        // User left the page - track as exit
        trackPageExit(pathname);
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      // Track exit when component unmounts (route change)
      if (pathname) {
        trackPageExit(pathname);
      }
      window.removeEventListener('beforeunload', handleBeforeUnload);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [pathname]);

  return null; // This component doesn't render anything
}
