'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

export default function ReferralLink() {
  const [referralCode, setReferralCode] = useState<string | null>(null);
  const [referralUrl, setReferralUrl] = useState<string | null>(null);
  const [stats, setStats] = useState<{
    total_referrals: number;
    completed_referrals: number;
    credits_earned: number;
  } | null>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    loadReferralData();
  }, []);

  const loadReferralData = async () => {
    try {
      setLoading(true);
      const [codeData, statsData] = await Promise.all([
        api.getReferralCode(),
        api.getReferralStats()
      ]);
      setReferralCode(codeData.referral_code);
      setReferralUrl(codeData.referral_url);
      setStats(statsData);
    } catch (error) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to load referral data');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    if (referralUrl) {
      try {
        await navigator.clipboard.writeText(referralUrl);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      } catch (error) {
        if (process.env.NODE_ENV === 'development') {
          console.error('Failed to copy');
        }
      }
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg border border-gray-200 p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-6 bg-gray-200 rounded w-1/3"></div>
          <div className="h-10 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Referral Program</h3>
      
      <div className="space-y-4">
        {/* Referral Link */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Your Referral Link
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={referralUrl || ''}
              readOnly
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg bg-gray-50 text-sm"
            />
            <button
              onClick={handleCopy}
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm"
            >
              {copied ? 'Copied!' : 'Copy'}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Share this link with friends. You'll both get credits when they sign up!
          </p>
        </div>

        {/* Stats */}
        {stats && (
          <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-200">
            <div className="text-center">
              <p className="text-2xl font-bold text-gray-900">{stats.total_referrals}</p>
              <p className="text-xs text-gray-600">Total Referrals</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">{stats.completed_referrals}</p>
              <p className="text-xs text-gray-600">Completed</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-blue-600">{stats.credits_earned}</p>
              <p className="text-xs text-gray-600">Credits Earned</p>
            </div>
          </div>
        )}

        {/* Info */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
          <p className="text-sm text-blue-800">
            <strong>How it works:</strong> Share your referral link. When someone signs up using your link and completes their first conversion, you both receive bonus credits!
          </p>
        </div>
      </div>
    </div>
  );
}

