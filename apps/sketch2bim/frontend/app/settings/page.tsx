'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useSession } from 'next-auth/react';
import Link from 'next/link';
import { api, User } from '@/lib/api';

export default function SettingsPage() {
  const router = useRouter();
  const { data: session, status } = useSession();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const loadUser = useCallback(async () => {
    setLoading(true);
    try {
      const data = await api.getCurrentUser();
      setUser(data);
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to load user:', err);
      }
      // Don't redirect here - session check is done separately
      // This might be a temporary API error, not an auth issue
    } finally {
      setLoading(false);
    }
  }, []);

  // Check session first before making API calls
  useEffect(() => {
    if (status === 'loading') {
      // Still loading session, wait
      return;
    }

    if (!session) {
      // No session, redirect to sign-in
      router.push('/api/auth/signin');
      return;
    }

    // Session exists, load user data
    loadUser();
  }, [session, status, router, loadUser]);

  const getTierBadge = (tier: string) => {
    switch (tier) {
      case 'trial':
        return '🆓 Trial';
      case 'week':
        return '📅 Week Access';
      case 'month':
        return '📦 Monthly';
      case 'year':
        return '💎 Yearly';
      default:
        return tier;
    }
  };

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'trial':
        return 'bg-gray-100 text-gray-800';
      case 'week':
        return 'bg-blue-100 text-blue-800';
      case 'month':
        return 'bg-purple-100 text-purple-800';
      case 'year':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const creditLabel =
    user?.subscription_tier === 'trial'
      ? `${user.credits} of 5 trial credits`
      : 'Unlimited conversions';

  const statusLabel = user?.subscription_status
    ? user.subscription_status.charAt(0).toUpperCase() + user.subscription_status.slice(1)
    : 'Inactive';

  const statusColor =
    user?.subscription_status === 'active'
      ? 'bg-green-100 text-green-800'
      : user?.subscription_status === 'expired'
      ? 'bg-amber-100 text-amber-800'
      : 'bg-gray-100 text-gray-800';

  // Show loading while checking session or loading user data
  if (status === 'loading' || loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  // If no session, redirect will happen in useEffect
  // If session exists but user data failed to load, show error or empty state
  if (!session || !user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <nav className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <Link href="/" className="text-2xl font-bold text-primary-600">
              Sketch-to-BIM
            </Link>
            <div className="flex items-center gap-4">
              <Link href="/dashboard" className="text-gray-700 dark:text-gray-300 hover:text-primary-600">
                Dashboard
              </Link>
              <Link href="/pricing" className="text-gray-700 dark:text-gray-300 hover:text-primary-600">
                Pricing
              </Link>
              <span className="text-gray-500 dark:text-gray-400">{user.email}</span>
              <form action="/api/auth/signout" method="POST">
                <button type="submit" className="text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-100">
                  Sign Out
                </button>
              </form>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">Settings</h1>
          <p className="text-gray-600 dark:text-gray-400">Manage your account settings and preferences</p>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Profile Section */}
          <div className="lg:col-span-2 space-y-6">
            {/* Account Information */}
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Account Information</h2>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Email
                  </label>
                  <div className="text-gray-900 dark:text-gray-100">{user.email}</div>
                </div>
                {user.name && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Name
                    </label>
                    <div className="text-gray-900 dark:text-gray-100">{user.name}</div>
                  </div>
                )}
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Subscription Tier
                  </label>
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getTierColor(user.subscription_tier)}`}>
                    {getTierBadge(user.subscription_tier)}
                  </span>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Subscription Status
                  </label>
                  <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${statusColor}`}>
                    {statusLabel}
                  </span>
                </div>
                <div className="space-y-1">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Credits Available
                  </label>
                  <div className="text-2xl font-bold text-primary-600 dark:text-primary-400">{creditLabel}</div>
                </div>
                {user.subscription_expires_at && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Access Expires
                    </label>
                    <div className="text-gray-900 dark:text-gray-100">
                      {new Date(user.subscription_expires_at).toLocaleString('en-IN', {
                        year: 'numeric',
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </div>
                  </div>
                )}
                {user.subscription_auto_renew !== undefined && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Auto-Renew
                    </label>
                    <div className="text-gray-900 dark:text-gray-100">
                      {user.subscription_auto_renew ? 'Yes (Subscription)' : 'No (One-time)'}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Subscription Management */}
            {user.razorpay_subscription_id && user.subscription_auto_renew && (
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">Subscription Management</h2>
                <div className="space-y-4">
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                    <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">
                      You have an active subscription that will auto-renew. You can cancel anytime and your access will continue until the end of your billing period.
                    </p>
                  </div>
                  {user.subscription_status === 'cancelled' ? (
                    <button
                      onClick={async () => {
                        if (!user.razorpay_subscription_id) return;
                        try {
                          await api.resumeSubscription(user.razorpay_subscription_id);
                          alert('Subscription resumed successfully!');
                          loadUser();
                        } catch (err: any) {
                          alert('Failed to resume subscription. Please try again.');
                        }
                      }}
                      className="w-full px-4 py-3 bg-primary-600 text-white rounded-lg text-center hover:bg-primary-700 transition-colors"
                    >
                      Resume Subscription
                    </button>
                  ) : (
                    <button
                      onClick={async () => {
                        if (!user.razorpay_subscription_id) return;
                        if (!confirm('Are you sure you want to cancel your subscription? Your access will continue until the end of your billing period.')) {
                          return;
                        }
                        try {
                          await api.cancelSubscription(user.razorpay_subscription_id);
                          alert('Subscription cancelled. Your access will continue until the end of your billing period.');
                          loadUser();
                        } catch (err: any) {
                          alert('Failed to cancel subscription. Please try again.');
                        }
                      }}
                      className="w-full px-4 py-3 bg-red-600 text-white rounded-lg text-center hover:bg-red-700 transition-colors"
                    >
                      Cancel Subscription
                    </button>
                  )}
                </div>
              </div>
            )}

            {/* Quick Actions */}
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
              <div className="space-y-3">
                {user.subscription_tier === 'trial' && (
                  <Link
                    href="/pricing"
                    className="block w-full px-4 py-3 bg-primary-600 text-white rounded-lg text-center hover:bg-primary-700 transition-colors"
                  >
                    View Paid Plans
                  </Link>
                )}
                <Link
                  href="/settings/payments"
                  className="block w-full px-4 py-3 border border-gray-300 dark:border-gray-700 rounded-lg text-center hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
                >
                  View Payment History
                </Link>
              </div>
            </div>
          </div>

          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <div className="card sticky top-8">
              <h3 className="font-semibold text-gray-900 dark:text-gray-100 mb-4">Settings</h3>
              <nav className="space-y-2">
                <Link
                  href="/settings"
                  className="block px-4 py-2 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-400 rounded-lg font-medium"
                >
                  Profile
                </Link>
                <Link
                  href="/settings/payments"
                  className="block px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg"
                >
                  Payment History
                </Link>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}


