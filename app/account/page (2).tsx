'use client';

import { useEffect, useState } from 'react';
import { useAuth } from '@/lib/auth-provider';
import { Card, Button } from '@kushalsamant/design-template';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { logger } from '@/lib/logger';

// Disable static generation for this page
export const dynamic = 'force-dynamic';

interface SubscriptionInfo {
  tier: string | null;
  status: string | null;
  expires_at: string | null;
  plan_name: string | null;
}

export default function AccountPage() {
  const { user, session, loading: authLoading, signOut } = useAuth();
  const router = useRouter();
  const [subscription, setSubscription] = useState<SubscriptionInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Wait for auth to load before making decisions
    if (authLoading) {
      return;
    }

    // Only redirect if we're definitely unauthenticated (not just loading)
    if (!user || !session) {
      router.push('/api/auth/signin');
      return;
    }

    // Load subscription data when authenticated
    if (user && session) {
      loadSubscription();
    }
  }, [authLoading, user, session, router]);

  const loadSubscription = async () => {
    try {
      const response = await fetch('/api/subscriptions/status');
      if (response.ok) {
        const data = await response.json();
        setSubscription(data);
      }
    } catch (error) {
      logger.error('Failed to load subscription:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCancelSubscription = async () => {
    if (!confirm('Are you sure you want to cancel your subscription? You will lose access to all platform apps at the end of your current billing period.')) {
      return;
    }

    try {
      const response = await fetch('/api/subscriptions/cancel', {
        method: 'POST',
      });

      if (response.ok) {
        alert('Subscription cancelled. You will retain access until the end of your billing period.');
        loadSubscription();
      } else {
        alert('Failed to cancel subscription. Please try again.');
      }
    } catch (error) {
      logger.error('Failed to cancel subscription:', error);
      alert('Failed to cancel subscription. Please try again.');
    }
  };

  const handleResumeSubscription = async () => {
    try {
      const response = await fetch('/api/subscriptions/resume', {
        method: 'POST',
      });

      if (response.ok) {
        alert('Subscription resumed successfully.');
        loadSubscription();
      } else {
        alert('Failed to resume subscription. Please try again.');
      }
    } catch (error) {
      logger.error('Failed to resume subscription:', error);
      alert('Failed to resume subscription. Please try again.');
    }
  };

  const handleSignOut = async () => {
    try {
      await signOut();
      router.push('/');
    } catch (error) {
      logger.error('Failed to sign out:', error);
      alert('Failed to sign out. Please try again.');
    }
  };

  if (authLoading || loading) {
    return (
      <div style={{ padding: 'var(--space-xl)', textAlign: 'center' }}>
        <div>Loading...</div>
      </div>
    );
  }

  if (!session || !user) {
    return null;
  }

  const hasActiveSubscription = subscription?.status === 'active';
  const isCancelled = subscription?.status === 'cancelled';

  return (
    <div style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
      <h1 style={{ fontSize: 'var(--font-size-4xl)', marginBottom: 'var(--space-xl)' }}>
        Account & Subscription
      </h1>

      {/* User Info */}
      <Card variant="default" style={{ marginBottom: 'var(--space-lg)' }}>
        <div style={{ padding: 'var(--space-lg)' }}>
          <h2 style={{ fontSize: 'var(--font-size-2xl)', marginBottom: 'var(--space-md)' }}>
            Account Information
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
            <div>
              <strong>Email:</strong> {user.email}
            </div>
            <div>
              <strong>Name:</strong> {user.user_metadata?.full_name || user.user_metadata?.name || 'Not provided'}
            </div>
          </div>
          <div style={{ marginTop: 'var(--space-md)', paddingTop: 'var(--space-md)', borderTop: '1px solid var(--color-border)' }}>
            <Button variant="secondary" onClick={handleSignOut}>
              Sign Out
            </Button>
          </div>
        </div>
      </Card>

      {/* Subscription Info */}
      <Card variant="default" style={{ marginBottom: 'var(--space-lg)' }}>
        <div style={{ padding: 'var(--space-lg)' }}>
          <h2 style={{ fontSize: 'var(--font-size-2xl)', marginBottom: 'var(--space-md)' }}>
            Subscription Status
          </h2>
          
          {!subscription?.tier ? (
            <div>
              <p style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text-secondary)' }}>
                You don't have an active subscription. Subscribe to get access to all KVSHVL platform apps.
              </p>
              <Link href="/subscribe">
                <Button variant="primary">Subscribe Now</Button>
              </Link>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-md)' }}>
              <div>
                <strong>Plan:</strong> {subscription.plan_name || subscription.tier}
              </div>
              <div>
                <strong>Status:</strong> {subscription.status}
              </div>
              {subscription.expires_at && (
                <div>
                  <strong>Expires:</strong> {new Date(subscription.expires_at).toLocaleDateString()}
                </div>
              )}
              
              <div style={{ marginTop: 'var(--space-md)', display: 'flex', gap: 'var(--space-sm)' }}>
                {hasActiveSubscription && !isCancelled && (
                  <Button variant="secondary" onClick={handleCancelSubscription}>
                    Cancel Subscription
                  </Button>
                )}
                {isCancelled && (
                  <Button variant="primary" onClick={handleResumeSubscription}>
                    Resume Subscription
                  </Button>
                )}
                <Link href="/subscribe">
                  <Button variant="secondary">Change Plan</Button>
                </Link>
              </div>
            </div>
          )}
        </div>
      </Card>

      {/* App Access */}
      <Card variant="default">
        <div style={{ padding: 'var(--space-lg)' }}>
          <h2 style={{ fontSize: 'var(--font-size-2xl)', marginBottom: 'var(--space-md)' }}>
            Platform Apps
          </h2>
          <p style={{ marginBottom: 'var(--space-md)', color: 'var(--color-text-secondary)' }}>
            Your subscription gives you access to Sketch2BIM:
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-sm)' }}>
            <Link href="https://sketch2bim.kvshvl.in" style={{ textDecoration: 'none', color: 'inherit' }}>
              <Button variant="secondary" style={{ width: '100%', justifyContent: 'flex-start' }}>
                Sketch2BIM →
              </Button>
            </Link>
          </div>
        </div>
      </Card>
    </div>
  );
}

