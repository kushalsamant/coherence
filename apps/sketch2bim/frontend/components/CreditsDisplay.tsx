'use client';

import { useEffect, useState } from 'react';
import { api, User } from '@/lib/api';
import Link from 'next/link';

export default function CreditsDisplay() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const data = await api.getCurrentUser();
      setUser(data);
    } catch (err) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to load user');
      }
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-gray-400">Loading...</div>;
  }

  if (!user) {
    return null;
  }

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'trial':
        return 'text-gray-600';
      case 'week':
        return 'text-blue-600';
      case 'monthly':
        return 'text-purple-600';
      case 'yearly':
        return 'text-green-600';
      default:
        return 'text-gray-600';
    }
  };

  const getTierBadge = (tier: string) => {
    switch (tier) {
      case 'trial':
        return '🆓 Trial';
      case 'week':
        return '📅 Week Access';
      case 'monthly':
        return '📦 Monthly';
      case 'yearly':
        return '💎 Yearly';
      default:
        return tier;
    }
  };

  const isTrial = user.subscription_tier === 'trial';
  const isActiveTrial = isTrial && user.subscription_status === 'active' && 
    (user.subscription_expires_at ? new Date(user.subscription_expires_at) > new Date() : false);
  const isPaidTier = !isTrial && ['week', 'monthly', 'yearly'].includes(user.subscription_tier);
  const isActivePaid = isPaidTier && user.subscription_status === 'active' && 
    (user.subscription_expires_at ? new Date(user.subscription_expires_at) > new Date() : false);
  
  let statusLabel: string;
  if (isActiveTrial) {
    statusLabel = 'Unlimited conversions - Trial active';
  } else if (isTrial) {
    statusLabel = 'Trial expired - Upgrade to continue';
  } else if (isActivePaid) {
    statusLabel = `Unlimited conversions - ${user.subscription_tier.charAt(0).toUpperCase() + user.subscription_tier.slice(1)} active`;
  } else {
    statusLabel = 'Subscription expired - Upgrade to continue';
  }

  return (
    <div className="flex items-center gap-4">
      <div className="text-right">
        <div className={`text-sm font-semibold ${getTierColor(user.subscription_tier)}`}>
          {getTierBadge(user.subscription_tier)}
        </div>
        <div className="text-xs text-gray-500">{statusLabel}</div>
      </div>
      
      {(isTrial || (!isActivePaid && isPaidTier)) && (
        <Link
          href="/pricing"
          className="px-3 py-1.5 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700 transition-colors"
        >
          {isTrial ? 'Upgrade' : 'Renew'}
        </Link>
      )}
    </div>
  );
}

