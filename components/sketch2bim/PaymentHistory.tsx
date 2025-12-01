'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import Link from 'next/link';

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

export default function PaymentHistory() {
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
    } finally {
      setLoading(false);
    }
  };

  const formatAmount = (amount: number, currency: string) => {
    const dollars = amount / 100;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency.toUpperCase()
    }).format(dollars);
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'succeeded':
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return <div className="text-center py-4">Loading payment history...</div>;
  }

  if (error) {
    return (
      <div className="card bg-red-50 border-red-200">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  if (payments.length === 0) {
    return (
      <div className="card text-center py-8">
        <p className="text-gray-600 mb-4">No payment history yet</p>
        <Link href="/pricing" className="text-primary-600 hover:text-primary-700">
          View Pricing →
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {payments.map((payment) => (
        <div key={payment.id} className="card">
          <div className="flex items-center justify-between">
            <div>
              <div className="font-semibold text-gray-900">{formatAmount(payment.amount, payment.currency)}</div>
              <div className="text-sm text-gray-600">
                {payment.product_type} • {new Date(payment.completed_at || payment.created_at).toLocaleDateString()}
              </div>
              <div className="text-sm text-gray-500">
                +{payment.credits_added} credits
              </div>
            </div>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(payment.status)}`}>
              {payment.status}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
}

