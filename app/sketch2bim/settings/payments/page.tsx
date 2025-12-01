'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { api } from '@/lib/sketch2bim/api';

interface Payment {
  id: number;
  amount: number;
  currency: string;
  status: string;
  product_type: string;
  credits_added: number;
  created_at: string;
  completed_at?: string;
}

export default function PaymentHistoryPage() {
  const router = useRouter();
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadPayments();
  }, []);

  const loadPayments = async () => {
    try {
      const data = await api.getPaymentHistory();
      setPayments(data);
      setError(null);
    } catch (err: any) {
      if (process.env.NODE_ENV === 'development') {
        console.error('Failed to load payments');
      }
      setError('Failed to load payment history');
      // Check status without exposing full error
      const status = err?.response?.status;
      if (status === 401) {
        router.push('/api/auth/signin');
      }
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const formatAmount = (amount: number, currency: string) => {
    // Razorpay amounts are in paise (₹1 = 100 paise)
    const mainAmount = amount / 100;
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: currency.toUpperCase() === 'INR' ? 'INR' : currency.toUpperCase()
    }).format(mainAmount);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'succeeded':
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getProductTypeLabel = (type: string) => {
    switch (type) {
      case 'single':
      case 'one_time':
        return 'Single Conversion';
      case 'week':
        return 'Week Access';
      case 'monthly':
        return 'Monthly Access';
      case 'yearly':
        return 'Yearly Access';
      case 'trial':
        return 'Trial';
      default:
        return type;
    }
  };

  const getCreditsLabel = (payment: Payment) => {
    if (['week', 'monthly', 'yearly'].includes(payment.product_type)) {
      return 'Unlimited';
    }
    return `${payment.credits_added} ${payment.credits_added === 1 ? 'credit' : 'credits'}`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
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
              <Link href="/settings" className="text-gray-700 dark:text-gray-300 hover:text-primary-600">
                Settings
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <Link href="/settings" className="text-primary-600 hover:text-primary-700 mb-4 inline-block">
            ← Back to Settings
          </Link>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">Payment History</h1>
          <p className="text-gray-600 dark:text-gray-400">View all your transactions and subscription history</p>
        </div>

        {error && (
          <div className="card bg-red-50 border-red-200 mb-6">
            <p className="text-red-800">{error}</p>
          </div>
        )}

        {payments.length === 0 ? (
          <div className="card text-center py-12">
            <div className="text-6xl mb-4">💳</div>
            <h3 className="text-xl font-semibold text-gray-700 dark:text-gray-300 mb-2">
              No payments yet
            </h3>
            <p className="text-gray-500 dark:text-gray-400 mb-6">
              Your payment history will appear here after your first purchase.
            </p>
            <Link
              href="/pricing"
              className="inline-block px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
            >
              View Pricing
            </Link>
          </div>
        ) : (
          <div className="card overflow-hidden">
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Date
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Product
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Amount
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Credits Added
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-gray-800">
                  {payments.map((payment) => (
                    <tr key={payment.id} className="hover:bg-gray-50 dark:hover:bg-gray-800">
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                        {formatDate(payment.completed_at || payment.created_at)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                        {getProductTypeLabel(payment.product_type)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-gray-100">
                        {formatAmount(payment.amount, payment.currency)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 dark:text-gray-100">
                        {getCreditsLabel(payment)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusColor(payment.status)}`}>
                          {payment.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

