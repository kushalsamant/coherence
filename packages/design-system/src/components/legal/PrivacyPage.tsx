import React from 'react'

interface PrivacyPageProps {
  appName?: string
  LinkComponent?: React.ComponentType<any>
}

export default function PrivacyPage({
  appName = 'Our Service',
  LinkComponent,
}: PrivacyPageProps) {
  const Link = LinkComponent || (({ href, className, children, ...props }: any) => (
    <a href={href} className={className} {...props}>{children}</a>
  ))

  return (
    <>
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. Introduction</h2>
        <p className="text-gray-700 mb-4">
          {appName} ("we," "our," or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our Service.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. Information We Collect</h2>
        <h3 className="text-xl font-semibold text-gray-900 mb-3">2.1 Account Information</h3>
        <p className="text-gray-700 mb-4">
          When you sign up using Google authentication, we collect:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Email address</li>
          <li>Name (if provided by Google)</li>
          <li>Google account ID</li>
        </ul>

        <h3 className="text-xl font-semibold text-gray-900 mb-3">2.2 Usage Information</h3>
        <p className="text-gray-700 mb-4">
          We collect information about how you use the Service, including:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Uploaded content and generated files</li>
          <li>Job processing history</li>
          <li>Subscription and payment information</li>
          <li>IP address and browser information</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. How We Use Your Information</h2>
        <p className="text-gray-700 mb-4">We use the information we collect to:</p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Provide, maintain, and improve the Service</li>
          <li>Process your uploads and generate files</li>
          <li>Manage your account and subscriptions</li>
          <li>Process payments through Razorpay</li>
          <li>Send you service-related communications</li>
          <li>Detect and prevent fraud or abuse</li>
          <li>Comply with legal obligations</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. Data Storage and Security</h2>
        <p className="text-gray-700 mb-4">
          Your uploaded content and generated files are stored securely. We implement appropriate technical and organizational measures to protect your data against unauthorized access, alteration, disclosure, or destruction.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. Third-Party Services</h2>
        <p className="text-gray-700 mb-4">We use the following third-party services:</p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li><strong>Google Authentication:</strong> For user authentication</li>
          <li><strong>Razorpay:</strong> For payment processing</li>
          <li><strong>Storage Services:</strong> For file storage and delivery</li>
        </ul>
        <p className="text-gray-700 mb-4">
          These services have their own privacy policies. We encourage you to review them.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Data Sharing</h2>
        <p className="text-gray-700 mb-4">
          We do not sell, trade, or rent your personal information to third parties. We may share your information only:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>With your explicit consent</li>
          <li>To comply with legal obligations</li>
          <li>To protect our rights and safety</li>
          <li>With service providers who assist in operating the Service (under confidentiality agreements)</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Your Rights</h2>
        <p className="text-gray-700 mb-4">You have the right to:</p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Access your personal data</li>
          <li>Correct inaccurate data</li>
          <li>Request deletion of your data</li>
          <li>Export your data</li>
          <li>Opt-out of marketing communications</li>
          <li>Cancel your subscription at any time</li>
        </ul>
        <p className="text-gray-700 mb-4">
          To exercise these rights, please contact us through <Link href="/contact" className="text-primary-600 hover:underline">our contact page</Link>.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">8. Cookies and Tracking</h2>
        <p className="text-gray-700 mb-4">
          We use cookies and similar tracking technologies to track activity on our Service and store certain information. You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">9. Children's Privacy</h2>
        <p className="text-gray-700 mb-4">
          Our Service is not intended for children under 18 years of age. We do not knowingly collect personal information from children under 18.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">10. Changes to Privacy Policy</h2>
        <p className="text-gray-700 mb-4">
          We may update this Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last updated" date.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">11. Contact Us</h2>
        <p className="text-gray-700 mb-4">
          If you have any questions about this Privacy Policy, please contact us at <Link href="/contact" className="text-primary-600 hover:underline">our contact page</Link>.
        </p>
      </section>
    </>
  )
}

