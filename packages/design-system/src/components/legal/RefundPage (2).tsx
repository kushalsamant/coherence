import React from 'react'

interface RefundPageProps {
  LinkComponent?: React.ComponentType<any>
}

export default function RefundPage({
  LinkComponent,
}: RefundPageProps) {
  const Link = LinkComponent || (({ href, className, children, ...props }: any) => (
    <a href={href} className={className} {...props}>{children}</a>
  ))

  return (
    <>
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. Subscription Cancellation</h2>
        <p className="text-gray-700 mb-4">
          You may cancel your subscription at any time from your account settings. When you cancel:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Your subscription will not auto-renew at the end of the current billing period</li>
          <li>You will continue to have access to all features until the end of your paid period</li>
          <li>No refunds are provided for the remaining period after cancellation</li>
          <li>You can resume your subscription at any time before it expires</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. Refund Policy</h2>
        
        <h3 className="text-xl font-semibold text-gray-900 mb-3">2.1 One-Time Payments</h3>
        <p className="text-gray-700 mb-4">
          One-time payments are non-refundable once the service has been accessed. If you experience technical issues that prevent you from using the service, please contact us within 24 hours of purchase.
        </p>

        <h3 className="text-xl font-semibold text-gray-900 mb-3">2.2 Subscription Refunds</h3>
        <p className="text-gray-700 mb-4">
          Monthly and Yearly subscriptions are eligible for a full refund within 7 days of the initial purchase, provided:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>You have not used more than 10% of your conversion quota</li>
          <li>The refund request is made within 7 days of purchase</li>
          <li>No chargeback or dispute has been initiated</li>
        </ul>

        <h3 className="text-xl font-semibold text-gray-900 mb-3">2.3 Non-Refundable Items</h3>
        <p className="text-gray-700 mb-4">The following are not eligible for refunds:</p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>One-time purchases after service has been accessed</li>
          <li>Subscriptions cancelled after 7 days</li>
          <li>Subscriptions where significant usage has occurred</li>
          <li>Refunds requested due to user error</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. How to Request a Refund</h2>
        <p className="text-gray-700 mb-4">
          To request a refund, please contact us through <Link href="/contact" className="text-primary-600 hover:underline">our contact page</Link> with:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Your account email address</li>
          <li>Order or payment ID</li>
          <li>Reason for refund request</li>
          <li>Date of purchase</li>
        </ul>
        <p className="text-gray-700 mb-4">
          We will review your request and respond within 5-7 business days. Approved refunds will be processed to your original payment method within 10-14 business days.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. Chargebacks and Disputes</h2>
        <p className="text-gray-700 mb-4">
          If you initiate a chargeback or dispute with your payment provider, we reserve the right to suspend your account until the matter is resolved. We encourage you to contact us first to resolve any issues before initiating a chargeback.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. Service Issues</h2>
        <p className="text-gray-700 mb-4">
          If you experience technical issues that prevent you from using the Service:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Contact us immediately through <Link href="/contact" className="text-primary-600 hover:underline">our contact page</Link></li>
          <li>We will investigate and attempt to resolve the issue</li>
          <li>If the issue cannot be resolved, we may offer a refund or service credit</li>
          <li>Refunds for technical issues are evaluated on a case-by-case basis</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Subscription Changes</h2>
        <p className="text-gray-700 mb-4">
          You can upgrade or downgrade your subscription at any time:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li><strong>Upgrades:</strong> Take effect immediately. You will be charged the prorated difference.</li>
          <li><strong>Downgrades:</strong> Take effect at the end of your current billing period. No refunds for the difference.</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Contact Information</h2>
        <p className="text-gray-700 mb-4">
          For questions about cancellations or refunds, please contact us at <Link href="/contact" className="text-primary-600 hover:underline">our contact page</Link>.
        </p>
      </section>
    </>
  )
}

