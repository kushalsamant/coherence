import React from 'react'

interface TermsPageProps {
  appName?: string
  serviceDescription?: string
  LinkComponent?: React.ComponentType<any>
}

export default function TermsPage({
  appName = 'Our Service',
  serviceDescription = 'web-based service',
  LinkComponent,
}: TermsPageProps) {
  const Link = LinkComponent || (({ href, className, children, ...props }: any) => (
    <a href={href} className={className} {...props}>{children}</a>
  ))

  return (
    <>
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. Acceptance of Terms</h2>
        <p className="text-gray-700 mb-4">
          By accessing and using {appName} ("the Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by the above, please do not use this service.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. Description of Service</h2>
        <p className="text-gray-700 mb-4">
          {appName} is a {serviceDescription}. The Service uses artificial intelligence and computer vision to process uploaded content.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. User Accounts</h2>
        <p className="text-gray-700 mb-4">
          To use the Service, you must create an account using your Google account. You are responsible for maintaining the confidentiality of your account credentials and for all activities that occur under your account.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. Subscription and Payment</h2>
        <p className="text-gray-700 mb-4">
          The Service offers various subscription tiers. All payments are processed through Razorpay. By subscribing, you agree to pay the fees associated with your chosen tier.
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Subscriptions automatically renew unless cancelled</li>
          <li>You can cancel your subscription at any time from your account settings</li>
          <li>Refunds are subject to our Cancellation and Refund Policy</li>
          <li>Prices are subject to change with 30 days notice</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. Use of Service</h2>
        <p className="text-gray-700 mb-4">You agree to use the Service only for lawful purposes and in accordance with these Terms. You agree not to:</p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Upload malicious code, viruses, or harmful content</li>
          <li>Attempt to reverse engineer or decompile the Service</li>
          <li>Use the Service to violate any laws or regulations</li>
          <li>Interfere with or disrupt the Service or servers</li>
          <li>Use automated systems to access the Service without permission</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Intellectual Property</h2>
        <p className="text-gray-700 mb-4">
          You retain all rights to the content you upload. The Service and its original content, features, and functionality are owned by {appName} and are protected by international copyright, trademark, patent, trade secret, and other intellectual property laws.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Limitation of Liability</h2>
        <p className="text-gray-700 mb-4">
          {appName} shall not be liable for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of profits, data, use, goodwill, or other intangible losses, resulting from your use of the Service.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">8. Disclaimer</h2>
        <p className="text-gray-700 mb-4">
          The Service is provided "as is" and "as available" without any warranties of any kind, either express or implied. We do not warrant that the Service will be uninterrupted, secure, or error-free.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">9. Changes to Terms</h2>
        <p className="text-gray-700 mb-4">
          We reserve the right to modify these Terms at any time. We will notify users of any material changes via email or through the Service. Your continued use of the Service after such modifications constitutes acceptance of the updated Terms.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">10. Contact Information</h2>
        <p className="text-gray-700 mb-4">
          If you have any questions about these Terms, please contact us at <Link href="/contact" className="text-primary-600 hover:underline">our contact page</Link>.
        </p>
      </section>
    </>
  )
}

