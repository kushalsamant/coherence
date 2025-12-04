import React from 'react'

interface ShippingPageProps {
  LinkComponent?: React.ComponentType<any>
}

export default function ShippingPage({
  LinkComponent,
}: ShippingPageProps) {
  const Link = LinkComponent || (({ href, className, children, ...props }: any) => (
    <a href={href} className={className} {...props}>{children}</a>
  ))

  return (
    <>
      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">1. Digital Service Delivery</h2>
        <p className="text-gray-700 mb-4">
          This is a digital service that processes content and delivers files electronically. There is no physical shipping involved. All deliverables are provided through digital download.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">2. File Delivery</h2>
        <p className="text-gray-700 mb-4">
          Upon successful processing:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Generated files are available for immediate download</li>
          <li>Files are accessible through your dashboard for the duration of your subscription</li>
          <li>Download links are provided via secure, time-limited URLs</li>
          <li>Files are stored securely for fast global access</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">3. Processing Time</h2>
        <p className="text-gray-700 mb-4">
          Processing times vary based on content complexity:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li><strong>Simple content:</strong> 2-5 minutes</li>
          <li><strong>Complex content:</strong> 5-15 minutes</li>
          <li><strong>Large files or batch uploads:</strong> 15-30 minutes</li>
        </ul>
        <p className="text-gray-700 mb-4">
          You will receive email notifications when processing is complete. Files are available immediately upon completion.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">4. File Retention</h2>
        <p className="text-gray-700 mb-4">
          Files are retained according to your subscription tier. We recommend downloading your files promptly. We are not responsible for files deleted after the retention period.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">5. File Formats and Compatibility</h2>
        <p className="text-gray-700 mb-4">
          We provide files in multiple formats. Files are generated using industry-standard tools. While we strive for compatibility, we cannot guarantee compatibility with all software versions. Please verify file compatibility with your software.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">6. Re-processing and Exchanges</h2>
        <p className="text-gray-700 mb-4">
          If you need to re-process content:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>You can upload the same content again (counts as a new conversion)</li>
          <li>Use variation features to generate alternative arrangements</li>
          <li>Use iteration features to make modifications to existing outputs</li>
          <li>Re-processing follows the same pricing as new uploads</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">7. Download Issues</h2>
        <p className="text-gray-700 mb-4">
          If you experience issues downloading files:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Check your internet connection</li>
          <li>Try a different browser</li>
          <li>Verify the download link hasn't expired</li>
          <li>Contact support if issues persist</li>
        </ul>
        <p className="text-gray-700 mb-4">
          We will assist in resolving download issues and may provide alternative download methods if needed.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">8. Data Export</h2>
        <p className="text-gray-700 mb-4">
          You can export your data at any time:
        </p>
        <ul className="list-disc pl-6 text-gray-700 mb-4">
          <li>Download all generated files from your dashboard</li>
          <li>Request a data export through <Link href="/contact" className="text-primary-600 hover:underline">our contact page</Link></li>
          <li>Data exports are provided in standard formats</li>
        </ul>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">9. International Access</h2>
        <p className="text-gray-700 mb-4">
          Our Service is accessible globally. Files are delivered through a Content Delivery Network (CDN) to ensure fast download speeds worldwide. No additional shipping charges apply.
        </p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">10. Contact Information</h2>
        <p className="text-gray-700 mb-4">
          For questions about file delivery or download issues, please contact us at <Link href="/contact" className="text-primary-600 hover:underline">our contact page</Link>.
        </p>
      </section>
    </>
  )
}

